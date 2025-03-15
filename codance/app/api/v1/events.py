from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ...core.database import get_db
from ...core.auth import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.event import Event, UserEvent, DetectedPattern
from ...schemas.event import (
    Event as EventSchema,
    EventCreate,
    EventUpdate,
    UserEvent as UserEventSchema,
    UserEventCreate,
    UserEventUpdate
)

router = APIRouter()

# Event Endpoints

@router.post("/", response_model=EventSchema)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new event (admin only).
    """
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[EventSchema])
async def read_events(
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all events, optionally filtered by active status.
    """
    query = db.query(Event)
    if is_active is not None:
        query = query.filter(Event.is_active == is_active)
    
    events = query.offset(skip).limit(limit).all()
    return events

@router.get("/upcoming", response_model=List[EventSchema])
async def read_upcoming_events(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get upcoming events within the specified number of days.
    """
    now = datetime.utcnow()
    end_date = now + timedelta(days=days)
    
    events = db.query(Event).filter(
        Event.start_time >= now,
        Event.start_time <= end_date
    ).order_by(Event.start_time).all()
    
    return events

@router.get("/{event_id}", response_model=EventSchema)
async def read_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get specific event by ID.
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update event by ID (admin only).
    """
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    event_dict = event_update.dict(exclude_unset=True)
    for key, value in event_dict.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete event by ID (admin only).
    """
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return None

# User Event Endpoints

@router.post("/register", response_model=UserEventSchema)
async def register_for_event(
    user_event: UserEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Register a user for an event.
    Users can only register themselves unless they are admins.
    """
    # Check if the user exists
    user = db.query(User).filter(User.id == user_event.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the event exists
    event = db.query(Event).filter(Event.id == user_event.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if user is registering themselves or is an admin
    if not current_user.is_admin and current_user.id != user_event.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to register other users for events"
        )
    
    # Check if user is already registered for this event
    existing_registration = db.query(UserEvent).filter(
        UserEvent.user_id == user_event.user_id,
        UserEvent.event_id == user_event.event_id
    ).first()
    
    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered for this event")
    
    # Create new user event registration
    db_user_event = UserEvent(**user_event.dict())
    db.add(db_user_event)
    db.commit()
    db.refresh(db_user_event)
    return db_user_event

@router.get("/registrations", response_model=List[UserEventSchema])
async def read_event_registrations(
    event_id: int = None,
    user_id: int = None,
    is_active: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get event registrations, optionally filtered by event_id, user_id, or active status.
    Regular users can only see their own registrations.
    """
    query = db.query(UserEvent)
    
    # If not admin, restrict to own registrations
    if not current_user.is_admin:
        query = query.filter(UserEvent.user_id == current_user.id)
    elif user_id:
        query = query.filter(UserEvent.user_id == user_id)
    
    if event_id:
        query = query.filter(UserEvent.event_id == event_id)
    
    if is_active is not None:
        query = query.filter(UserEvent.is_active == is_active)
    
    registrations = query.offset(skip).limit(limit).all()
    return registrations

@router.put("/registrations/{registration_id}", response_model=UserEventSchema)
async def update_event_registration(
    registration_id: int,
    registration_update: UserEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update event registration by ID.
    Users can only update their own registrations unless they are admins.
    """
    db_registration = db.query(UserEvent).filter(UserEvent.id == registration_id).first()
    if db_registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Check if user has permission to update this registration
    if not current_user.is_admin and db_registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this registration"
        )
    
    # Update fields
    registration_dict = registration_update.dict(exclude_unset=True)
    for key, value in registration_dict.items():
        setattr(db_registration, key, value)
    
    db.commit()
    db.refresh(db_registration)
    return db_registration

@router.delete("/registrations/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete event registration by ID.
    Users can only delete their own registrations unless they are admins.
    """
    db_registration = db.query(UserEvent).filter(UserEvent.id == registration_id).first()
    if db_registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Check if user has permission to delete this registration
    if not current_user.is_admin and db_registration.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this registration"
        )
    
    db.delete(db_registration)
    db.commit()
    return None

# Check-in/Check-out Endpoints

@router.post("/checkin", response_model=UserEventSchema)
async def checkin_to_event(
    event_id: int,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Check in a user to an event.
    Users can only check themselves in unless they are admins.
    """
    # If user_id not provided, use current user's ID
    if user_id is None:
        user_id = current_user.id
    elif not current_user.is_admin and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check in other users"
        )
    
    # Find the registration
    registration = db.query(UserEvent).filter(
        UserEvent.user_id == user_id,
        UserEvent.event_id == event_id,
        UserEvent.is_active == True
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Active registration not found")
    
    # Update check-in time
    registration.checkin_time = datetime.utcnow()
    db.commit()
    db.refresh(registration)
    return registration

@router.post("/checkout", response_model=UserEventSchema)
async def checkout_from_event(
    event_id: int,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Check out a user from an event.
    Users can only check themselves out unless they are admins.
    """
    # If user_id not provided, use current user's ID
    if user_id is None:
        user_id = current_user.id
    elif not current_user.is_admin and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check out other users"
        )
    
    # Find the registration
    registration = db.query(UserEvent).filter(
        UserEvent.user_id == user_id,
        UserEvent.event_id == event_id,
        UserEvent.is_active == True
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Active registration not found")
    
    # Update check-out time
    registration.checkout_time = datetime.utcnow()
    db.commit()
    db.refresh(registration)
    return registration 