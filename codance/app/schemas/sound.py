from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, bytes
from datetime import datetime

# Sound Event schemas
class SoundEventBase(BaseModel):
    event_id: int
    movement_data_id: Optional[int] = None
    sound_type: str
    parameters: Dict[str, Any]
    duration: float
    intensity: float

class SoundEventCreate(SoundEventBase):
    pass

class SoundEventUpdate(BaseModel):
    sound_type: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None
    intensity: Optional[float] = None

class SoundEvent(SoundEventBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Song Selection schemas
class SongSelectionBase(BaseModel):
    user_id: int
    event_id: int
    song_title: str
    artist: str
    duration: float
    audio_features: Optional[Dict[str, Any]] = None
    is_approved: bool = False

class SongSelectionCreate(SongSelectionBase):
    pass

class SongSelectionUpdate(BaseModel):
    audio_features: Optional[Dict[str, Any]] = None
    is_approved: Optional[bool] = None

class SongSelection(SongSelectionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Sound Sample schemas
class SoundSampleBase(BaseModel):
    name: str
    category: str
    sample_data: bytes  # Binary data
    duration: float
    sample_rate: int

class SoundSampleCreate(SoundSampleBase):
    pass

class SoundSample(SoundSampleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Sound Preset schemas
class SoundPresetBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]

class SoundPresetCreate(SoundPresetBase):
    pass

class SoundPresetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class SoundPreset(SoundPresetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 