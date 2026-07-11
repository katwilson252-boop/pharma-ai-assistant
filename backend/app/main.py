from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import Base, engine
from app.routes import interactions, chat

# Create database tables (for demo/assignment)
# In production, use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM - HCP Module API",
    version="1.0.0",
    description="AI-powered CRM backend for Healthcare Professional (HCP) interactions.",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(interactions.router)
app.include_router(chat.router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Pharma AI Assistant API is running successfully!",
        "docs": "/docs",
        "health": "/api/health",
    }


# Health check
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "message": "API is healthy",
    }