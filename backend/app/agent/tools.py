import json
import datetime as dt
from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.db.models import HCP, Interaction
from app.agent.llm import call_llm


def _get_or_create_hcp(db, name: str) -> HCP:
    hcp = db.query(HCP).filter(HCP.name.ilike(name)).first()
    if not hcp:
        hcp = HCP(name=name)
        db.add(hcp)
        db.commit()
        db.refresh(hcp)
    return hcp


# ---------------------------------------------------------------------------
# Tool 1 (required): log_interaction
# ---------------------------------------------------------------------------
@tool
def log_interaction(free_text: str, hcp_name: str = "") -> str:
    """
    Log a new HCP interaction from free-form natural language, e.g.
    "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure".
    Uses the LLM to extract structured entities (HCP name, topics, sentiment,
    materials, samples, outcomes, follow-ups) from the free text, then saves
    a new Interaction row to the database. Returns the created interaction as JSON.
    """
    extraction_prompt = f"""
Extract structured CRM data from this field rep's note about a healthcare
professional (HCP) interaction. Return ONLY valid JSON, no other text, with
this exact schema:

{{
  "hcp_name": "string",
  "interaction_type": "Meeting|Call|Email|Conference",
  "topics_discussed": "string",
  "materials_shared": ["string"],
  "samples_distributed": ["string"],
  "sentiment": "Positive|Neutral|Negative",
  "outcomes": "string",
  "follow_up_actions": ["string"]
}}

Note: "{free_text}"
Known HCP name hint (use if the note doesn't clearly state one): "{hcp_name}"
"""
    raw = call_llm(extraction_prompt, system="You are a precise healthcare CRM data-extraction assistant.")

    try:
        cleaned = raw.strip().strip("`").replace("json\n", "", 1)
        data = json.loads(cleaned)
    except Exception:
        data = {
            "hcp_name": hcp_name or "Unknown HCP",
            "interaction_type": "Meeting",
            "topics_discussed": free_text,
            "materials_shared": [],
            "samples_distributed": [],
            "sentiment": "Neutral",
            "outcomes": "",
            "follow_up_actions": [],
        }

    db = SessionLocal()
    try:
        hcp = _get_or_create_hcp(db, data.get("hcp_name") or hcp_name or "Unknown HCP")
        interaction = Interaction(
            hcp_id=hcp.id,
            interaction_type=data.get("interaction_type", "Meeting"),
            interaction_datetime=dt.datetime.utcnow(),
            attendees=[],
            topics_discussed=data.get("topics_discussed", ""),
            materials_shared=data.get("materials_shared", []),
            samples_distributed=data.get("samples_distributed", []),
            sentiment=data.get("sentiment", "Neutral"),
            outcomes=data.get("outcomes", ""),
            follow_up_actions=data.get("follow_up_actions", []),
            raw_source="chat",
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return json.dumps({
            "id": interaction.id,
            "hcp_name": hcp.name,
            "interaction_type": interaction.interaction_type,
            "topics_discussed": interaction.topics_discussed,
            "sentiment": interaction.sentiment,
            "materials_shared": interaction.materials_shared,
            "samples_distributed": interaction.samples_distributed,
            "outcomes": interaction.outcomes,
            "follow_up_actions": interaction.follow_up_actions,
        })
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 2 (required): edit_interaction
# ---------------------------------------------------------------------------
@tool
def edit_interaction(interaction_id: str, updates_free_text: str) -> str:
    """
    Edit an already-logged interaction. Takes the interaction_id and a
    free-text description of what should change, e.g. "actually sentiment
    was negative, and add a follow-up to send the Phase III PDF". Uses the
    LLM to turn that into a partial update, then applies it to the database
    row. Returns the updated interaction as JSON, or an error message if not found.
    """
    db = SessionLocal()
    try:
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return json.dumps({"error": f"No interaction found with id {interaction_id}"})

        current = {
            "interaction_type": interaction.interaction_type,
            "topics_discussed": interaction.topics_discussed,
            "materials_shared": interaction.materials_shared,
            "samples_distributed": interaction.samples_distributed,
            "sentiment": interaction.sentiment,
            "outcomes": interaction.outcomes,
            "follow_up_actions": interaction.follow_up_actions,
        }

        prompt = f"""
Current interaction record (JSON): {json.dumps(current)}

The user wants this change applied: "{updates_free_text}"

Return ONLY the JSON fields that should change, using the same schema as the
current record. Do not include unchanged fields.
"""
        raw = call_llm(prompt, system="You output only valid partial-update JSON, nothing else.")
        cleaned = raw.strip().strip("`").replace("json\n", "", 1)
        changes = json.loads(cleaned)

        for field, value in changes.items():
            if hasattr(interaction, field):
                setattr(interaction, field, value)

        interaction.updated_at = dt.datetime.utcnow()
        db.commit()
        db.refresh(interaction)

        return json.dumps({
            "id": interaction.id,
            "interaction_type": interaction.interaction_type,
            "topics_discussed": interaction.topics_discussed,
            "sentiment": interaction.sentiment,
            "materials_shared": interaction.materials_shared,
            "samples_distributed": interaction.samples_distributed,
            "outcomes": interaction.outcomes,
            "follow_up_actions": interaction.follow_up_actions,
        })
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 3: get_hcp_history
# ---------------------------------------------------------------------------
@tool
def get_hcp_history(hcp_name: str) -> str:
    """
    Retrieve the interaction history for a given HCP by name, so the agent
    (or the rep) has context on past visits, sentiment trends, and prior
    commitments before logging a new interaction.
    """
    db = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return json.dumps({"error": f"No HCP found matching '{hcp_name}'"})

        history = [
            {
                "date": i.interaction_datetime.isoformat() if i.interaction_datetime else None,
                "type": i.interaction_type,
                "topics": i.topics_discussed,
                "sentiment": i.sentiment,
                "outcomes": i.outcomes,
            }
            for i in hcp.interactions
        ]
        return json.dumps({"hcp_name": hcp.name, "history": history})
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tool 4: suggest_followups
# ---------------------------------------------------------------------------
@tool
def suggest_followups(interaction_summary: str) -> str:
    """
    Given a summary of what was discussed in an interaction, suggest 2-4
    concrete, actionable follow-up tasks for the field rep (e.g. scheduling
    a follow-up meeting, sending literature, adding the HCP to an advisory
    board list). Returns a JSON list of suggestion strings.
    """
    prompt = f"""
Based on this HCP interaction summary, suggest 2-4 concrete follow-up actions
a pharma field rep should take. Return ONLY a JSON array of short strings.

Summary: "{interaction_summary}"
"""
    raw = call_llm(prompt, system="You are a helpful pharma sales-ops assistant. Output only a JSON array.")
    try:
        cleaned = raw.strip().strip("`").replace("json\n", "", 1)
        suggestions = json.loads(cleaned)
    except Exception:
        suggestions = [raw.strip()]
    return json.dumps(suggestions)


# ---------------------------------------------------------------------------
# Tool 5: check_compliance_flags
# ---------------------------------------------------------------------------
@tool
def check_compliance_flags(interaction_summary: str) -> str:
    """
    Scan an interaction summary for potential compliance concerns relevant to
    pharma-HCP engagement (e.g. off-label discussion, excessive gifting,
    undisclosed samples) and flag anything that should be reviewed by
    Medical/Legal before the interaction is finalized. Returns JSON with a
    boolean 'flagged' field and a 'reason' string.
    """
    prompt = f"""
Review this pharma field-rep interaction summary for compliance concerns such
as off-label promotion, excessive gifting, or unlogged sample distribution.
Return ONLY JSON: {{"flagged": true|false, "reason": "string, empty if not flagged"}}

Summary: "{interaction_summary}"
"""
    raw = call_llm(prompt, system="You are a pharma compliance reviewer. Output only valid JSON.")
    try:
        cleaned = raw.strip().strip("`").replace("json\n", "", 1)
        result = json.loads(cleaned)
    except Exception:
        result = {"flagged": False, "reason": ""}
    return json.dumps(result)


ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    get_hcp_history,
    suggest_followups,
    check_compliance_flags,
]
