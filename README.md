# AI-First CRM – HCP Module: Log Interaction Screen

An AI-first "Log HCP Interaction" screen for pharma field reps. Reps can log
a visit either through a structured form **or** by chatting naturally with an
AI assistant, which is backed by a LangGraph agent running on Groq LLMs.

## Architecture

```
Frontend (React + Redux)  ──HTTP──►  Backend (FastAPI)
     │                                     │
     │  structured form  ───────────►  /api/interactions  ──► Postgres
     │                                     │
     └  chat messages    ───────────►  /api/chat
                                            │
                                    LangGraph Agent
                                    (Groq gemma2-9b-it,
                                     fallback llama-3.3-70b-versatile)
                                            │
                                     5 Tools (see below)
```

### LangGraph agent's role

The agent sits behind the chat panel and acts as the rep's assistant for the
entire interaction lifecycle: understanding a free-text description of a
visit, deciding which tool(s) to call, pulling historical context when
useful, writing structured data to the database, and proactively suggesting
next steps — all without the rep touching the form.

### The 5 tools

| Tool | Purpose |
|---|---|
| `log_interaction` (required) | Takes free text, uses the LLM to extract HCP name, topics, sentiment, materials/samples, outcomes, and follow-ups as JSON, then writes a new `Interaction` row. |
| `edit_interaction` (required) | Takes an `interaction_id` + a free-text description of the change, uses the LLM to compute a partial update, and applies it to the existing row. |
| `get_hcp_history` | Looks up all past interactions for a named HCP so the agent has context before logging/advising. |
| `suggest_followups` | Given an interaction summary, proposes 2–4 concrete next-step actions (mirrors the "AI Suggested Follow-ups" panel in the mock). |
| `check_compliance_flags` | Screens a summary for pharma-compliance concerns (off-label talk, excessive gifting, etc.) before the interaction is finalized. |

## Tech stack

- **Frontend:** React 18, Redux Toolkit, Google Inter font
- **Backend:** Python, FastAPI
- **Agent framework:** LangGraph
- **LLM:** Groq — `gemma2-9b-it` primary, `llama-3.3-70b-versatile` fallback
- **Database:** PostgreSQL via SQLAlchemy (swap-able to MySQL, see backend `.env.example`)

## Prerequisites

- Python 3.11+
- Node.js 18+
- A running PostgreSQL instance (local install or Docker)
- A free Groq API key from https://console.groq.com

## Setup — Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set GROQ_API_KEY and DATABASE_URL

# make sure the database in DATABASE_URL exists, e.g.:
# createdb hcp_crm

uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000` (docs at `/docs`).

## Setup — Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

Opens at `http://localhost:3000`.

## Using the app

- **Form path:** fill in the left-hand card and click "Log Interaction".
- **Chat path:** type something like *"Met Dr. Sharma, discussed OncoBoost
  Phase III data, she seemed positive, shared the brochure and left a sample"*
  into the AI Assistant panel. The agent extracts structured fields and saves
  the interaction automatically, then can suggest follow-ups if you ask
  "what should I do next?".
- **Editing via chat:** reference the interaction id returned by the agent,
  e.g. *"for interaction <id>, change sentiment to negative and add a
  follow-up to send the Phase III PDF"*.

## Project structure

```
backend/
  app/
    agent/
      llm.py        # Groq client wrapper w/ fallback model
      tools.py       # the 5 LangGraph tools
      graph.py       # LangGraph StateGraph wiring
    db/
      models.py      # HCP, Interaction SQLAlchemy models
      database.py    # engine/session
    routes/
      interactions.py  # structured-form CRUD endpoints
      chat.py           # conversational endpoint
    schemas.py       # Pydantic request/response models
    config.py        # env-based settings
    main.py          # FastAPI app + CORS + router registration
  requirements.txt
  .env.example

frontend/
  src/
    components/
      InteractionForm.js     # structured form (left panel)
      ChatAssistant.js        # AI chat panel (right panel)
      LogInteractionScreen.js # combines both
    redux/
      interactionSlice.js    # form state + async thunks
      store.js
    api/client.js            # fetch wrapper for the FastAPI backend
    styles/global.css        # Inter font + layout
  package.json
  .env.example
```

## Notes / what I understood from the task

The brief asks for a "Log Interaction" screen that lets a rep choose between
a structured form and a conversational interface, backed by a mandatory
LangGraph + LLM agent with at least 5 tools (including log/edit). I
implemented both entry points against a shared FastAPI + Postgres backend so
a logged interaction looks identical regardless of which path created it,
and built the agent so the two required tools (log/edit) do the heavy lifting
of LLM-based entity extraction, while three supporting tools (history,
follow-up suggestions, compliance check) round out realistic sales-rep
workflows a life-sciences CRM would need.
