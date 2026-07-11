import datetime as dt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import HCP, Interaction
from app.schemas import InteractionCreate, InteractionUpdate, InteractionOut

router = APIRouter(prefix="/api/interactions", tags=["interactions"])


def _to_out(interaction: Interaction) -> InteractionOut:
    return InteractionOut(
        id=interaction.id,
        hcp_id=interaction.hcp_id,
        hcp_name=interaction.hcp.name,
        interaction_type=interaction.interaction_type,
        interaction_datetime=interaction.interaction_datetime,
        attendees=interaction.attendees or [],
        topics_discussed=interaction.topics_discussed,
        materials_shared=interaction.materials_shared or [],
        samples_distributed=interaction.samples_distributed or [],
        sentiment=interaction.sentiment,
        outcomes=interaction.outcomes,
        follow_up_actions=interaction.follow_up_actions or [],
        raw_source=interaction.raw_source,
    )


@router.get("", response_model=list[InteractionOut])
def list_interactions(db: Session = Depends(get_db)):
    return [_to_out(i) for i in db.query(Interaction).order_by(Interaction.created_at.desc()).all()]


@router.post("", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.name.ilike(payload.hcp_name)).first()
    if not hcp:
        hcp = HCP(name=payload.hcp_name)
        db.add(hcp)
        db.commit()
        db.refresh(hcp)

    interaction = Interaction(
        hcp_id=hcp.id,
        interaction_type=payload.interaction_type,
        interaction_datetime=payload.interaction_datetime or dt.datetime.utcnow(),
        attendees=payload.attendees,
        topics_discussed=payload.topics_discussed,
        materials_shared=payload.materials_shared,
        samples_distributed=payload.samples_distributed,
        sentiment=payload.sentiment,
        outcomes=payload.outcomes,
        follow_up_actions=payload.follow_up_actions,
        raw_source="form",
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return _to_out(interaction)


@router.patch("/{interaction_id}", response_model=InteractionOut)
def update_interaction(interaction_id: str, payload: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(interaction, field, value)
    interaction.updated_at = dt.datetime.utcnow()

    db.commit()
    db.refresh(interaction)
    return _to_out(interaction)


@router.get("/{interaction_id}", response_model=InteractionOut)
def get_interaction(interaction_id: str, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return _to_out(interaction)
