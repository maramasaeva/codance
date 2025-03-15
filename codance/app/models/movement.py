from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base
from .event import DetectedPattern  # Import DetectedPattern from event module

class MovementData(Base):
    __tablename__ = "movement_data"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data_type = Column(String)  # e.g., "heatmap", "trajectory", "gesture"
    coordinates = Column(JSON)  # JSON storing coordinate data
    velocity = Column(Float, nullable=True)
    acceleration = Column(Float, nullable=True)
    crowd_density = Column(Float, nullable=True)
    movement_intensity = Column(Float, nullable=True)
    
    # Relationships with lazy loading
    event = relationship("Event", back_populates="movement_data", lazy="joined")
    sound_events = relationship("SoundEvent", back_populates="movement_data", lazy="dynamic")

class MovementPattern(Base):
    __tablename__ = "movement_patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    pattern_data = Column(JSON)  # Stored pattern for recognition
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships with lazy loading
    detected_patterns = relationship("DetectedPattern", back_populates="pattern", lazy="dynamic") 