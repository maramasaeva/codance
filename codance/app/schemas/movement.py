from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Movement Data schemas
class MovementDataBase(BaseModel):
    event_id: int
    data_type: str
    coordinates: Dict[str, Any]
    velocity: Optional[float] = None
    acceleration: Optional[float] = None
    crowd_density: Optional[float] = None
    movement_intensity: Optional[float] = None

class MovementDataCreate(MovementDataBase):
    pass

class MovementDataUpdate(BaseModel):
    data_type: Optional[str] = None
    coordinates: Optional[Dict[str, Any]] = None
    velocity: Optional[float] = None
    acceleration: Optional[float] = None
    crowd_density: Optional[float] = None
    movement_intensity: Optional[float] = None

class MovementData(MovementDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Movement Pattern schemas
class MovementPatternBase(BaseModel):
    name: str
    description: Optional[str] = None
    pattern_data: Dict[str, Any]

class MovementPatternCreate(MovementPatternBase):
    pass

class MovementPatternUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    pattern_data: Optional[Dict[str, Any]] = None

class MovementPattern(MovementPatternBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Detected Pattern schemas
class DetectedPatternBase(BaseModel):
    pattern_id: int
    event_id: int
    confidence: float

class DetectedPatternCreate(DetectedPatternBase):
    pass

class DetectedPattern(DetectedPatternBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True 