from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Biometric Data schemas
class BiometricDataBase(BaseModel):
    user_id: int
    event_id: int
    device_id: str
    heart_rate: Optional[float] = None
    gsr: Optional[float] = None
    temperature: Optional[float] = None
    energy_level: Optional[float] = None
    emotional_state: Optional[str] = None

class BiometricDataCreate(BiometricDataBase):
    pass

class BiometricDataUpdate(BaseModel):
    heart_rate: Optional[float] = None
    gsr: Optional[float] = None
    temperature: Optional[float] = None
    energy_level: Optional[float] = None
    emotional_state: Optional[str] = None

class BiometricData(BiometricDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Biometric Device schemas
class BiometricDeviceBase(BaseModel):
    device_id: str
    device_type: str
    is_active: bool = True

class BiometricDeviceCreate(BiometricDeviceBase):
    pass

class BiometricDeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    is_active: Optional[bool] = None

class BiometricDevice(BiometricDeviceBase):
    id: int
    last_connection: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 