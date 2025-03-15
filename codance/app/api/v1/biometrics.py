from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import numpy as np
from datetime import datetime

from ...core.database import get_db
from ...core.auth import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.biometrics import BiometricData, BiometricDevice
from ...models.event import Event
from ...schemas.biometrics import (
    BiometricData as BiometricDataSchema,
    BiometricDataCreate,
    BiometricDataUpdate,
    BiometricDevice as BiometricDeviceSchema,
    BiometricDeviceCreate,
    BiometricDeviceUpdate
)

router = APIRouter()

@router.post("/data", response_model=BiometricDataSchema)
async def create_biometric_data(
    biometric_data: BiometricDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new biometric data record.
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == biometric_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the event exists
    event = db.query(Event).filter(Event.id == biometric_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Create new biometric data
    db_biometric_data = BiometricData(**biometric_data.dict())
    db.add(db_biometric_data)
    db.commit()
    db.refresh(db_biometric_data)
    return db_biometric_data

@router.get("/data", response_model=List[BiometricDataSchema])
async def read_biometric_data(
    user_id: int = None,
    event_id: int = None,
    device_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get biometric data, optionally filtered by user_id, event_id, or device_id.
    Users can only access their own data unless they are admins.
    """
    query = db.query(BiometricData)
    
    # If not admin, restrict to own data
    if not current_user.is_admin:
        query = query.filter(BiometricData.user_id == current_user.id)
    elif user_id:
        query = query.filter(BiometricData.user_id == user_id)
    
    if event_id:
        query = query.filter(BiometricData.event_id == event_id)
    
    if device_id:
        query = query.filter(BiometricData.device_id == device_id)
    
    biometric_data = query.offset(skip).limit(limit).all()
    return biometric_data

@router.get("/data/{biometric_data_id}", response_model=BiometricDataSchema)
async def read_biometric_data_by_id(
    biometric_data_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific biometric data by ID.
    Users can only access their own data unless they are admins.
    """
    biometric_data = db.query(BiometricData).filter(BiometricData.id == biometric_data_id).first()
    if biometric_data is None:
        raise HTTPException(status_code=404, detail="Biometric data not found")
    
    # Check if user has permission to access this data
    if not current_user.is_admin and biometric_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this biometric data"
        )
    
    return biometric_data

@router.put("/data/{biometric_data_id}", response_model=BiometricDataSchema)
async def update_biometric_data(
    biometric_data_id: int,
    biometric_data_update: BiometricDataUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update biometric data by ID.
    Users can only update their own data unless they are admins.
    """
    db_biometric_data = db.query(BiometricData).filter(BiometricData.id == biometric_data_id).first()
    if db_biometric_data is None:
        raise HTTPException(status_code=404, detail="Biometric data not found")
    
    # Check if user has permission to update this data
    if not current_user.is_admin and db_biometric_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this biometric data"
        )
    
    # Update fields
    biometric_data_dict = biometric_data_update.dict(exclude_unset=True)
    for key, value in biometric_data_dict.items():
        setattr(db_biometric_data, key, value)
    
    db.commit()
    db.refresh(db_biometric_data)
    return db_biometric_data

@router.delete("/data/{biometric_data_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_biometric_data(
    biometric_data_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete biometric data by ID.
    Users can only delete their own data unless they are admins.
    """
    db_biometric_data = db.query(BiometricData).filter(BiometricData.id == biometric_data_id).first()
    if db_biometric_data is None:
        raise HTTPException(status_code=404, detail="Biometric data not found")
    
    # Check if user has permission to delete this data
    if not current_user.is_admin and db_biometric_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this biometric data"
        )
    
    db.delete(db_biometric_data)
    db.commit()
    return None

# Biometric Device Endpoints

@router.post("/devices", response_model=BiometricDeviceSchema)
async def create_biometric_device(
    device: BiometricDeviceCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Register a new biometric device (admin only).
    """
    # Check if device ID already exists
    existing_device = db.query(BiometricDevice).filter(BiometricDevice.device_id == device.device_id).first()
    if existing_device:
        raise HTTPException(status_code=400, detail="Device ID already registered")
    
    db_device = BiometricDevice(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/devices", response_model=List[BiometricDeviceSchema])
async def read_biometric_devices(
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all biometric devices, optionally filtered by active status.
    """
    query = db.query(BiometricDevice)
    if is_active is not None:
        query = query.filter(BiometricDevice.is_active == is_active)
    
    devices = query.offset(skip).limit(limit).all()
    return devices

@router.get("/devices/{device_id}", response_model=BiometricDeviceSchema)
async def read_biometric_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific biometric device by ID.
    """
    device = db.query(BiometricDevice).filter(BiometricDevice.device_id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Biometric device not found")
    return device

@router.put("/devices/{device_id}", response_model=BiometricDeviceSchema)
async def update_biometric_device(
    device_id: str,
    device_update: BiometricDeviceUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update biometric device by ID (admin only).
    """
    db_device = db.query(BiometricDevice).filter(BiometricDevice.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Biometric device not found")
    
    # Update fields
    device_dict = device_update.dict(exclude_unset=True)
    for key, value in device_dict.items():
        setattr(db_device, key, value)
    
    # Update last_connection field
    db_device.last_connection = datetime.utcnow()
    
    db.commit()
    db.refresh(db_device)
    return db_device

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_biometric_device(
    device_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete biometric device by ID (admin only).
    """
    db_device = db.query(BiometricDevice).filter(BiometricDevice.device_id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Biometric device not found")
    
    db.delete(db_device)
    db.commit()
    return None

# Simulation endpoint for testing

@router.post("/simulate", response_model=BiometricDataSchema)
async def simulate_biometric_data(
    user_id: int,
    event_id: int,
    device_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Simulate biometric data for testing purposes.
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Generate simulated biometric data
    heart_rate = float(np.random.normal(80, 15))  # Mean 80 bpm with standard deviation of 15
    gsr = float(np.random.uniform(0.5, 5.0))  # Random GSR value
    temperature = float(np.random.normal(36.9, 0.5))  # Body temperature in Celsius
    energy_level = float(np.random.uniform(0, 1))  # Normalized energy level
    
    # Map energy level to emotional state
    emotional_states = ["calm", "excited", "joyful", "focused", "energetic"]
    emotional_state = emotional_states[int(energy_level * len(emotional_states))]
    
    # Create biometric data object
    biometric_data = BiometricData(
        user_id=user_id,
        event_id=event_id,
        device_id=device_id,
        heart_rate=heart_rate,
        gsr=gsr,
        temperature=temperature,
        energy_level=energy_level,
        emotional_state=emotional_state
    )
    
    db.add(biometric_data)
    db.commit()
    db.refresh(biometric_data)
    return biometric_data 