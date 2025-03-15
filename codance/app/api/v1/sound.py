from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime
import json

from ...core.database import get_db
from ...core.auth import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.sound import SoundEvent, SongSelection, SoundSample, SoundPreset
from ...models.event import Event
from ...models.movement import MovementData
from ...schemas.sound import (
    SoundEvent as SoundEventSchema,
    SoundEventCreate,
    SoundEventUpdate,
    SongSelection as SongSelectionSchema,
    SongSelectionCreate,
    SongSelectionUpdate,
    SoundSample as SoundSampleSchema,
    SoundSampleCreate,
    SoundPreset as SoundPresetSchema,
    SoundPresetCreate,
    SoundPresetUpdate
)

router = APIRouter()

# Sound Event Endpoints

@router.post("/events", response_model=SoundEventSchema)
async def create_sound_event(
    sound_event: SoundEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new sound event.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == sound_event.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if the movement data exists if provided
    if sound_event.movement_data_id:
        movement_data = db.query(MovementData).filter(MovementData.id == sound_event.movement_data_id).first()
        if not movement_data:
            raise HTTPException(status_code=404, detail="Movement data not found")
    
    # Create new sound event
    db_sound_event = SoundEvent(**sound_event.dict())
    db.add(db_sound_event)
    db.commit()
    db.refresh(db_sound_event)
    return db_sound_event

@router.get("/events", response_model=List[SoundEventSchema])
async def read_sound_events(
    event_id: int = None,
    sound_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get sound events, optionally filtered by event_id or sound_type.
    """
    query = db.query(SoundEvent)
    if event_id:
        query = query.filter(SoundEvent.event_id == event_id)
    if sound_type:
        query = query.filter(SoundEvent.sound_type == sound_type)
    
    sound_events = query.offset(skip).limit(limit).all()
    return sound_events

@router.get("/events/{sound_event_id}", response_model=SoundEventSchema)
async def read_sound_event(
    sound_event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific sound event by ID.
    """
    sound_event = db.query(SoundEvent).filter(SoundEvent.id == sound_event_id).first()
    if sound_event is None:
        raise HTTPException(status_code=404, detail="Sound event not found")
    return sound_event

@router.put("/events/{sound_event_id}", response_model=SoundEventSchema)
async def update_sound_event(
    sound_event_id: int,
    sound_event_update: SoundEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update sound event by ID.
    """
    db_sound_event = db.query(SoundEvent).filter(SoundEvent.id == sound_event_id).first()
    if db_sound_event is None:
        raise HTTPException(status_code=404, detail="Sound event not found")
    
    # Update fields
    sound_event_dict = sound_event_update.dict(exclude_unset=True)
    for key, value in sound_event_dict.items():
        setattr(db_sound_event, key, value)
    
    db.commit()
    db.refresh(db_sound_event)
    return db_sound_event

@router.delete("/events/{sound_event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sound_event(
    sound_event_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete sound event by ID (admin only).
    """
    db_sound_event = db.query(SoundEvent).filter(SoundEvent.id == sound_event_id).first()
    if db_sound_event is None:
        raise HTTPException(status_code=404, detail="Sound event not found")
    
    db.delete(db_sound_event)
    db.commit()
    return None

# Song Selection Endpoints

@router.post("/songs", response_model=SongSelectionSchema)
async def create_song_selection(
    song: SongSelectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new song selection.
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == song.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the event exists
    event = db.query(Event).filter(Event.id == song.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Create new song selection
    db_song = SongSelection(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@router.get("/songs", response_model=List[SongSelectionSchema])
async def read_song_selections(
    user_id: int = None,
    event_id: int = None,
    is_approved: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get song selections, optionally filtered by user_id, event_id, or approval status.
    """
    query = db.query(SongSelection)
    
    # If not admin, restrict to own songs
    if not current_user.is_admin:
        query = query.filter(SongSelection.user_id == current_user.id)
    elif user_id:
        query = query.filter(SongSelection.user_id == user_id)
    
    if event_id:
        query = query.filter(SongSelection.event_id == event_id)
    
    if is_approved is not None:
        query = query.filter(SongSelection.is_approved == is_approved)
    
    songs = query.offset(skip).limit(limit).all()
    return songs

@router.get("/songs/{song_id}", response_model=SongSelectionSchema)
async def read_song_selection(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific song selection by ID.
    """
    song = db.query(SongSelection).filter(SongSelection.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song selection not found")
    
    # Check if user has permission to access this song
    if not current_user.is_admin and song.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this song selection"
        )
    
    return song

@router.put("/songs/{song_id}", response_model=SongSelectionSchema)
async def update_song_selection(
    song_id: int,
    song_update: SongSelectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update song selection by ID.
    Regular users can only update audio_features, admins can approve songs.
    """
    db_song = db.query(SongSelection).filter(SongSelection.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song selection not found")
    
    # Check permissions
    if not current_user.is_admin and db_song.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this song selection"
        )
    
    # Regular users can't approve songs
    if not current_user.is_admin and song_update.is_approved is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to approve songs"
        )
    
    # Update fields
    song_dict = song_update.dict(exclude_unset=True)
    for key, value in song_dict.items():
        setattr(db_song, key, value)
    
    db.commit()
    db.refresh(db_song)
    return db_song

@router.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song_selection(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete song selection by ID.
    Users can only delete their own songs unless they are admins.
    """
    db_song = db.query(SongSelection).filter(SongSelection.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song selection not found")
    
    # Check if user has permission to delete this song
    if not current_user.is_admin and db_song.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this song selection"
        )
    
    db.delete(db_song)
    db.commit()
    return None

# Sound Preset Endpoints

@router.post("/presets", response_model=SoundPresetSchema)
async def create_sound_preset(
    preset: SoundPresetCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new sound preset (admin only).
    """
    db_preset = SoundPreset(**preset.dict())
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.get("/presets", response_model=List[SoundPresetSchema])
async def read_sound_presets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all sound presets.
    """
    presets = db.query(SoundPreset).offset(skip).limit(limit).all()
    return presets

@router.get("/presets/{preset_id}", response_model=SoundPresetSchema)
async def read_sound_preset(
    preset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific sound preset by ID.
    """
    preset = db.query(SoundPreset).filter(SoundPreset.id == preset_id).first()
    if preset is None:
        raise HTTPException(status_code=404, detail="Sound preset not found")
    return preset

@router.put("/presets/{preset_id}", response_model=SoundPresetSchema)
async def update_sound_preset(
    preset_id: int,
    preset_update: SoundPresetUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update sound preset by ID (admin only).
    """
    db_preset = db.query(SoundPreset).filter(SoundPreset.id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Sound preset not found")
    
    # Update fields
    preset_dict = preset_update.dict(exclude_unset=True)
    for key, value in preset_dict.items():
        setattr(db_preset, key, value)
    
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.delete("/presets/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sound_preset(
    preset_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete sound preset by ID (admin only).
    """
    db_preset = db.query(SoundPreset).filter(SoundPreset.id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Sound preset not found")
    
    db.delete(db_preset)
    db.commit()
    return None

# Simulation endpoint for testing

@router.post("/simulate", response_model=SoundEventSchema)
async def simulate_sound_event(
    event_id: int,
    movement_data_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Simulate a sound event for testing purposes.
    """
    # Check if the event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if the movement data exists if provided
    if movement_data_id:
        movement_data = db.query(MovementData).filter(MovementData.id == movement_data_id).first()
        if not movement_data:
            raise HTTPException(status_code=404, detail="Movement data not found")
    
    # Generate simulated sound parameters
    sound_types = ["bass", "percussion", "melody", "ambient", "vocal"]
    sound_type = np.random.choice(sound_types)
    
    # Create parameters based on sound type
    if sound_type == "bass":
        parameters = {
            "frequency": float(np.random.uniform(30, 120)),
            "resonance": float(np.random.uniform(0.1, 0.9)),
            "envelope": {
                "attack": float(np.random.uniform(0.01, 0.2)),
                "decay": float(np.random.uniform(0.1, 0.5)),
                "sustain": float(np.random.uniform(0.3, 0.8)),
                "release": float(np.random.uniform(0.2, 1.0))
            }
        }
    elif sound_type == "percussion":
        parameters = {
            "type": np.random.choice(["kick", "snare", "hihat", "clap"]),
            "pitch": float(np.random.uniform(0.5, 1.5)),
            "decay": float(np.random.uniform(0.1, 2.0)),
            "filter": {
                "cutoff": float(np.random.uniform(200, 8000)),
                "resonance": float(np.random.uniform(0.1, 0.9))
            }
        }
    else:
        parameters = {
            "waveform": np.random.choice(["sine", "square", "sawtooth", "triangle"]),
            "frequency": float(np.random.uniform(100, 1000)),
            "modulation": {
                "type": np.random.choice(["am", "fm", "none"]),
                "depth": float(np.random.uniform(0, 1)),
                "rate": float(np.random.uniform(0.1, 10))
            }
        }
    
    # Create sound event object
    sound_event = SoundEvent(
        event_id=event_id,
        movement_data_id=movement_data_id,
        sound_type=sound_type,
        parameters=parameters,
        duration=float(np.random.uniform(0.5, 5.0)),
        intensity=float(np.random.uniform(0, 1))
    )
    
    db.add(sound_event)
    db.commit()
    db.refresh(sound_event)
    return sound_event 