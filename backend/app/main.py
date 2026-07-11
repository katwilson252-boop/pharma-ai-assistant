from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import Base, engine
from app.routes import interactions, chat

# Creates tables if they don't exist yet (fine for an assignment/demo;
# use Alembic migrations for a real production system).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM - HCP Module API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interactions.router)
app.include_router(chat.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
