from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean, LargeBinary, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class SoundEvent(Base):
    __tablename__ = "sound_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    movement_data_id = Column(Integer, ForeignKey("movement_data.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sound_type = Column(String)  # e.g., "bass", "percussion", "melody", "ambient"
    parameters = Column(JSON)  # Sound generation parameters
    duration = Column(Float)  # Duration in seconds
    intensity = Column(Float)
    
    # Relationships with lazy loading
    event = relationship("Event", back_populates="sound_events", lazy="joined")
    movement_data = relationship("MovementData", back_populates="sound_events", lazy="joined")

class SongSelection(Base):
    __tablename__ = "song_selections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    song_title = Column(String)
    artist = Column(String)
    duration = Column(Float)  # Duration in seconds
    audio_features = Column(JSON, nullable=True)  # Extracted audio features
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships with lazy loading
    user = relationship("User", back_populates="song_selections", lazy="joined")
    event = relationship("Event", back_populates="song_selections", lazy="joined")

class SoundSample(Base):
    __tablename__ = "sound_samples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    sample_data = Column(LargeBinary)  # Binary audio data
    duration = Column(Float)  # Duration in seconds
    sample_rate = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class SoundPreset(Base):
    __tablename__ = "sound_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    parameters = Column(JSON)  # Preset parameters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 