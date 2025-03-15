from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base

class BiometricData(Base):
    __tablename__ = "biometric_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    device_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    heart_rate = Column(Float, nullable=True)
    gsr = Column(Float, nullable=True)  # Galvanic Skin Response
    temperature = Column(Float, nullable=True)
    energy_level = Column(Float, nullable=True)  # Calculated energy level
    emotional_state = Column(String, nullable=True)  # Inferred emotional state
    
    # Relationships
    user = relationship("User", back_populates="biometric_data")
    event = relationship("Event", back_populates="biometric_data")
    
class BiometricDevice(Base):
    __tablename__ = "biometric_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    device_type = Column(String)
    is_active = Column(Boolean, default=True)
    last_connection = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 