from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    location = Column(String)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=False)
    max_capacity = Column(Integer, nullable=True)
    configuration = Column(JSON, nullable=True)  # Event-specific configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships - Using lazy loading to avoid circular dependencies
    users = relationship("UserEvent", back_populates="event", lazy="dynamic")
    movement_data = relationship("MovementData", back_populates="event", lazy="dynamic")
    biometric_data = relationship("BiometricData", back_populates="event", lazy="dynamic")
    sound_events = relationship("SoundEvent", back_populates="event", lazy="dynamic")
    song_selections = relationship("SongSelection", back_populates="event", lazy="dynamic")
    visualization_events = relationship("VisualizationEvent", back_populates="event", lazy="dynamic")
    detected_patterns = relationship("DetectedPattern", back_populates="event", lazy="dynamic")

class UserEvent(Base):
    __tablename__ = "user_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    registration_time = Column(DateTime(timezone=True), server_default=func.now())
    checkin_time = Column(DateTime(timezone=True), nullable=True)
    checkout_time = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="events", lazy="joined")
    event = relationship("Event", back_populates="users", lazy="joined")

class DetectedPattern(Base):
    __tablename__ = "detected_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey("movement_patterns.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    confidence = Column(Float)  # Detection confidence score
    
    # Relationships
    pattern = relationship("MovementPattern", back_populates="detected_patterns", lazy="joined")
    event = relationship("Event", back_populates="detected_patterns", lazy="joined") 