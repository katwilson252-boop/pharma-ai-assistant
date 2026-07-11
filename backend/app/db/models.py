import uuid
import datetime as dt

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class HCP(Base):
    """A Healthcare Professional the field rep engages with."""
    __tablename__ = "hcps"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=True)
    hospital = Column(String(255), nullable=True)

    interactions = relationship("Interaction", back_populates="hcp")


class Interaction(Base):
    """A single logged interaction with an HCP."""
    __tablename__ = "interactions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    hcp_id = Column(String(36), ForeignKey("hcps.id"), nullable=False)

    interaction_type = Column(String(50), default="Meeting")  # Meeting/Call/Email/Conference
    interaction_datetime = Column(DateTime, default=dt.datetime.utcnow)

    attendees = Column(JSON, default=list)          # list[str]
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(JSON, default=list)    # list[str]
    samples_distributed = Column(JSON, default=list) # list[str]

    sentiment = Column(String(20), default="Neutral")  # Positive/Neutral/Negative
    outcomes = Column(Text, nullable=True)
    follow_up_actions = Column(JSON, default=list)   # list[str]

    raw_source = Column(String(20), default="form")  # "form" or "chat"
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")
