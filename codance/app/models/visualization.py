from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class VisualizationEvent(Base):
    __tablename__ = "visualization_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    visualization_type = Column(String)  # e.g., "holographic", "projection", "laser"
    parameters = Column(JSON)  # Visualization parameters
    duration = Column(Float)  # Duration in seconds
    intensity = Column(Float)
    
    # Relationships with lazy loading
    event = relationship("Event", back_populates="visualization_events", lazy="joined")

class VisualizationPreset(Base):
    __tablename__ = "visualization_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    parameters = Column(JSON)  # Preset parameters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 