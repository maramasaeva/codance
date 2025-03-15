from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime

from ...core.database import get_db
from ...core.auth import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.visualization import VisualizationEvent, VisualizationPreset
from ...models.event import Event
from ...models.movement import MovementData
from ...schemas.visualization import (
    VisualizationEvent as VisualizationEventSchema,
    VisualizationEventCreate,
    VisualizationEventUpdate,
    VisualizationPreset as VisualizationPresetSchema,
    VisualizationPresetCreate,
    VisualizationPresetUpdate
)

router = APIRouter()

# Visualization Event Endpoints

@router.post("/events", response_model=VisualizationEventSchema)
async def create_visualization_event(
    visualization_event: VisualizationEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new visualization event.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == visualization_event.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Create new visualization event
    db_visualization_event = VisualizationEvent(**visualization_event.dict())
    db.add(db_visualization_event)
    db.commit()
    db.refresh(db_visualization_event)
    return db_visualization_event

@router.get("/events", response_model=List[VisualizationEventSchema])
async def read_visualization_events(
    event_id: int = None,
    visualization_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get visualization events, optionally filtered by event_id or visualization_type.
    """
    query = db.query(VisualizationEvent)
    if event_id:
        query = query.filter(VisualizationEvent.event_id == event_id)
    if visualization_type:
        query = query.filter(VisualizationEvent.visualization_type == visualization_type)
    
    visualization_events = query.offset(skip).limit(limit).all()
    return visualization_events

@router.get("/events/{visualization_event_id}", response_model=VisualizationEventSchema)
async def read_visualization_event(
    visualization_event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific visualization event by ID.
    """
    visualization_event = db.query(VisualizationEvent).filter(VisualizationEvent.id == visualization_event_id).first()
    if visualization_event is None:
        raise HTTPException(status_code=404, detail="Visualization event not found")
    return visualization_event

@router.put("/events/{visualization_event_id}", response_model=VisualizationEventSchema)
async def update_visualization_event(
    visualization_event_id: int,
    visualization_event_update: VisualizationEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update visualization event by ID.
    """
    db_visualization_event = db.query(VisualizationEvent).filter(VisualizationEvent.id == visualization_event_id).first()
    if db_visualization_event is None:
        raise HTTPException(status_code=404, detail="Visualization event not found")
    
    # Update fields
    visualization_event_dict = visualization_event_update.dict(exclude_unset=True)
    for key, value in visualization_event_dict.items():
        setattr(db_visualization_event, key, value)
    
    db.commit()
    db.refresh(db_visualization_event)
    return db_visualization_event

@router.delete("/events/{visualization_event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visualization_event(
    visualization_event_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete visualization event by ID (admin only).
    """
    db_visualization_event = db.query(VisualizationEvent).filter(VisualizationEvent.id == visualization_event_id).first()
    if db_visualization_event is None:
        raise HTTPException(status_code=404, detail="Visualization event not found")
    
    db.delete(db_visualization_event)
    db.commit()
    return None

# Visualization Preset Endpoints

@router.post("/presets", response_model=VisualizationPresetSchema)
async def create_visualization_preset(
    preset: VisualizationPresetCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new visualization preset (admin only).
    """
    db_preset = VisualizationPreset(**preset.dict())
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.get("/presets", response_model=List[VisualizationPresetSchema])
async def read_visualization_presets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all visualization presets.
    """
    presets = db.query(VisualizationPreset).offset(skip).limit(limit).all()
    return presets

@router.get("/presets/{preset_id}", response_model=VisualizationPresetSchema)
async def read_visualization_preset(
    preset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific visualization preset by ID.
    """
    preset = db.query(VisualizationPreset).filter(VisualizationPreset.id == preset_id).first()
    if preset is None:
        raise HTTPException(status_code=404, detail="Visualization preset not found")
    return preset

@router.put("/presets/{preset_id}", response_model=VisualizationPresetSchema)
async def update_visualization_preset(
    preset_id: int,
    preset_update: VisualizationPresetUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update visualization preset by ID (admin only).
    """
    db_preset = db.query(VisualizationPreset).filter(VisualizationPreset.id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Visualization preset not found")
    
    # Update fields
    preset_dict = preset_update.dict(exclude_unset=True)
    for key, value in preset_dict.items():
        setattr(db_preset, key, value)
    
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.delete("/presets/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visualization_preset(
    preset_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete visualization preset by ID (admin only).
    """
    db_preset = db.query(VisualizationPreset).filter(VisualizationPreset.id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Visualization preset not found")
    
    db.delete(db_preset)
    db.commit()
    return None

# Simulation endpoint for testing

@router.post("/simulate", response_model=VisualizationEventSchema)
async def simulate_visualization_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Simulate a visualization event for testing purposes.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Generate simulated visualization parameters
    visualization_types = ["holographic", "projection", "laser", "led", "mist"]
    visualization_type = np.random.choice(visualization_types)
    
    # Create parameters based on visualization type
    if visualization_type == "holographic":
        parameters = {
            "density": float(np.random.uniform(0.1, 1.0)),
            "color": {
                "hue": float(np.random.uniform(0, 360)),
                "saturation": float(np.random.uniform(0.5, 1.0)),
                "brightness": float(np.random.uniform(0.5, 1.0))
            },
            "pattern": np.random.choice(["wave", "spiral", "pulse", "geometric"]),
            "rotation_speed": float(np.random.uniform(0, 10))
        }
    elif visualization_type == "projection":
        parameters = {
            "resolution": np.random.choice(["720p", "1080p", "4K"]),
            "brightness": float(np.random.uniform(0.5, 1.0)),
            "mapping": np.random.choice(["flat", "3d", "curved"]),
            "content": np.random.choice(["abstract", "geometric", "particle", "fluid"])
        }
    else:
        parameters = {
            "color_scheme": np.random.choice(["monochrome", "complementary", "analogous", "triadic"]),
            "speed": float(np.random.uniform(0.1, 5.0)),
            "complexity": float(np.random.uniform(0.1, 1.0)),
            "reactivity": float(np.random.uniform(0.1, 1.0))
        }
    
    # Create visualization event object
    visualization_event = VisualizationEvent(
        event_id=event_id,
        visualization_type=visualization_type,
        parameters=parameters,
        duration=float(np.random.uniform(0.5, 10.0)),
        intensity=float(np.random.uniform(0, 1))
    )
    
    db.add(visualization_event)
    db.commit()
    db.refresh(visualization_event)
    return visualization_event 