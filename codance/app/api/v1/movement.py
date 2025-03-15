from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import numpy as np
from datetime import datetime

from ...core.database import get_db
from ...core.auth import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.movement import MovementData, MovementPattern, DetectedPattern
from ...models.event import Event
from ...schemas.movement import (
    MovementData as MovementDataSchema,
    MovementDataCreate,
    MovementDataUpdate,
    MovementPattern as MovementPatternSchema,
    MovementPatternCreate,
    MovementPatternUpdate,
    DetectedPattern as DetectedPatternSchema,
    DetectedPatternCreate
)

router = APIRouter()

@router.post("/data", response_model=MovementDataSchema)
async def create_movement_data(
    movement_data: MovementDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new movement data record.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == movement_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Create new movement data
    db_movement_data = MovementData(**movement_data.dict())
    db.add(db_movement_data)
    db.commit()
    db.refresh(db_movement_data)
    return db_movement_data

@router.get("/data", response_model=List[MovementDataSchema])
async def read_movement_data(
    event_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get movement data, optionally filtered by event_id.
    """
    query = db.query(MovementData)
    if event_id:
        query = query.filter(MovementData.event_id == event_id)
    
    movement_data = query.offset(skip).limit(limit).all()
    return movement_data

@router.get("/data/{movement_data_id}", response_model=MovementDataSchema)
async def read_movement_data_by_id(
    movement_data_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific movement data by ID.
    """
    movement_data = db.query(MovementData).filter(MovementData.id == movement_data_id).first()
    if movement_data is None:
        raise HTTPException(status_code=404, detail="Movement data not found")
    return movement_data

@router.put("/data/{movement_data_id}", response_model=MovementDataSchema)
async def update_movement_data(
    movement_data_id: int,
    movement_data_update: MovementDataUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update movement data by ID.
    """
    db_movement_data = db.query(MovementData).filter(MovementData.id == movement_data_id).first()
    if db_movement_data is None:
        raise HTTPException(status_code=404, detail="Movement data not found")
    
    # Update fields
    movement_data_dict = movement_data_update.dict(exclude_unset=True)
    for key, value in movement_data_dict.items():
        setattr(db_movement_data, key, value)
    
    db.commit()
    db.refresh(db_movement_data)
    return db_movement_data

@router.delete("/data/{movement_data_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movement_data(
    movement_data_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete movement data by ID (admin only).
    """
    db_movement_data = db.query(MovementData).filter(MovementData.id == movement_data_id).first()
    if db_movement_data is None:
        raise HTTPException(status_code=404, detail="Movement data not found")
    
    db.delete(db_movement_data)
    db.commit()
    return None

# Movement Pattern Endpoints

@router.post("/patterns", response_model=MovementPatternSchema)
async def create_movement_pattern(
    pattern: MovementPatternCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new movement pattern (admin only).
    """
    db_pattern = MovementPattern(**pattern.dict())
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern

@router.get("/patterns", response_model=List[MovementPatternSchema])
async def read_movement_patterns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all movement patterns.
    """
    patterns = db.query(MovementPattern).offset(skip).limit(limit).all()
    return patterns

@router.get("/patterns/{pattern_id}", response_model=MovementPatternSchema)
async def read_movement_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific movement pattern by ID.
    """
    pattern = db.query(MovementPattern).filter(MovementPattern.id == pattern_id).first()
    if pattern is None:
        raise HTTPException(status_code=404, detail="Movement pattern not found")
    return pattern

@router.put("/patterns/{pattern_id}", response_model=MovementPatternSchema)
async def update_movement_pattern(
    pattern_id: int,
    pattern_update: MovementPatternUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update movement pattern by ID (admin only).
    """
    db_pattern = db.query(MovementPattern).filter(MovementPattern.id == pattern_id).first()
    if db_pattern is None:
        raise HTTPException(status_code=404, detail="Movement pattern not found")
    
    # Update fields
    pattern_dict = pattern_update.dict(exclude_unset=True)
    for key, value in pattern_dict.items():
        setattr(db_pattern, key, value)
    
    db.commit()
    db.refresh(db_pattern)
    return db_pattern

@router.delete("/patterns/{pattern_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movement_pattern(
    pattern_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete movement pattern by ID (admin only).
    """
    db_pattern = db.query(MovementPattern).filter(MovementPattern.id == pattern_id).first()
    if db_pattern is None:
        raise HTTPException(status_code=404, detail="Movement pattern not found")
    
    db.delete(db_pattern)
    db.commit()
    return None

# Detected Pattern Endpoints

@router.post("/detected-patterns", response_model=DetectedPatternSchema)
async def create_detected_pattern(
    detected_pattern: DetectedPatternCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new detected pattern record.
    """
    # Check if pattern exists
    pattern = db.query(MovementPattern).filter(MovementPattern.id == detected_pattern.pattern_id).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    
    # Check if event exists
    event = db.query(Event).filter(Event.id == detected_pattern.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_detected_pattern = DetectedPattern(**detected_pattern.dict())
    db.add(db_detected_pattern)
    db.commit()
    db.refresh(db_detected_pattern)
    return db_detected_pattern

@router.get("/detected-patterns", response_model=List[DetectedPatternSchema])
async def read_detected_patterns(
    event_id: int = None,
    pattern_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detected patterns, optionally filtered by event_id or pattern_id.
    """
    query = db.query(DetectedPattern)
    if event_id:
        query = query.filter(DetectedPattern.event_id == event_id)
    if pattern_id:
        query = query.filter(DetectedPattern.pattern_id == pattern_id)
    
    detected_patterns = query.offset(skip).limit(limit).all()
    return detected_patterns

# Simulation endpoint for testing

@router.post("/simulate", response_model=MovementDataSchema)
async def simulate_movement_data(
    event_id: int,
    num_dancers: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Simulate movement data for testing purposes.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Generate simulated movement data
    coordinates = {
        "dancers": []
    }
    
    # Create random dancer positions
    for i in range(num_dancers):
        coordinates["dancers"].append({
            "id": i,
            "x": float(np.random.uniform(0, 100)),
            "y": float(np.random.uniform(0, 100)),
            "velocity_x": float(np.random.uniform(-2, 2)),
            "velocity_y": float(np.random.uniform(-2, 2))
        })
    
    # Calculate crowd metrics
    avg_velocity = np.mean([
        np.sqrt(d["velocity_x"]**2 + d["velocity_y"]**2) 
        for d in coordinates["dancers"]
    ])
    
    # Create movement data object
    movement_data = MovementData(
        event_id=event_id,
        data_type="heatmap",
        coordinates=coordinates,
        velocity=float(avg_velocity),
        crowd_density=float(num_dancers / 100),
        movement_intensity=float(np.random.uniform(0, 1))
    )
    
    db.add(movement_data)
    db.commit()
    db.refresh(movement_data)
    return movement_data 