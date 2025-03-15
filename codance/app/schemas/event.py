from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Event schemas
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    start_time: datetime
    end_time: datetime
    is_active: bool = False
    max_capacity: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_active: Optional[bool] = None
    max_capacity: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# User Event schemas
class UserEventBase(BaseModel):
    user_id: int
    event_id: int
    is_active: bool = True

class UserEventCreate(UserEventBase):
    pass

class UserEventUpdate(BaseModel):
    checkin_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None
    is_active: Optional[bool] = None

class UserEvent(UserEventBase):
    id: int
    registration_time: datetime
    checkin_time: Optional[datetime] = None
    checkout_time: Optional[datetime] = None

    class Config:
        orm_mode = True 