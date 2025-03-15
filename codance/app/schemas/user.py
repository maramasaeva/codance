from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Base User schema
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for user in DB
class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schema for user response
class User(UserInDB):
    pass

# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    username: Optional[str] = None 