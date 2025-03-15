from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Visualization Event schemas
class VisualizationEventBase(BaseModel):
    event_id: int
    visualization_type: str
    parameters: Dict[str, Any]
    duration: float
    intensity: float

class VisualizationEventCreate(VisualizationEventBase):
    pass

class VisualizationEventUpdate(BaseModel):
    visualization_type: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None
    intensity: Optional[float] = None

class VisualizationEvent(VisualizationEventBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Visualization Preset schemas
class VisualizationPresetBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]

class VisualizationPresetCreate(VisualizationPresetBase):
    pass

class VisualizationPresetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class VisualizationPreset(VisualizationPresetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 