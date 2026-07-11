import datetime as dt
from typing import Optional

from pydantic import BaseModel


# -------------------------------------------------------------------
# Interaction Schemas
# -------------------------------------------------------------------

class InteractionBase(BaseModel):
    hcp_name: str
    interaction_type: str = "Meeting"
    interaction_datetime: Optional[dt.datetime] = None
    attendees: list[str] = []
    topics_discussed: Optional[str] = None
    materials_shared: list[str] = []
    samples_distributed: list[str] = []
    sentiment: str = "Neutral"
    outcomes: Optional[str] = None
    follow_up_actions: list[str] = []


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    interaction_datetime: Optional[dt.datetime] = None
    attendees: Optional[list[str]] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[list[str]] = None
    samples_distributed: Optional[list[str]] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up_actions: Optional[list[str]] = None


class InteractionOut(InteractionBase):
    id: str
    hcp_id: str
    raw_source: str

    class Config:
        from_attributes = True


# -------------------------------------------------------------------
# Chat Schemas
# -------------------------------------------------------------------

class ChatMessage(BaseModel):
    message: str
    interaction_id: Optional[str] = None


class LoggedInteraction(BaseModel):
    id: str
    hcp_name: str
    interaction_type: str
    topics_discussed: Optional[str] = None
    sentiment: str
    materials_shared: list[str] = []
    samples_distributed: list[str] = []
    outcomes: Optional[str] = None
    follow_up_actions: list[str] = []


class ChatResponse(BaseModel):
    reply: str
    tool_calls: list[str] = []
    interaction: Optional[LoggedInteraction] = None