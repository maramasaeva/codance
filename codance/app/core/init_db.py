from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from .database import SessionLocal, engine, Base
from .auth import get_password_hash

# Import all models so they're registered with SQLAlchemy
from ..models.user import User
from ..models.biometrics import BiometricData, BiometricDevice
from ..models.event import Event, UserEvent, DetectedPattern
from ..models.movement import MovementData, MovementPattern
from ..models.sound import SoundEvent, SongSelection, SoundSample, SoundPreset
from ..models.visualization import VisualizationEvent, VisualizationPreset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database with some sample data."""
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    
    # Simple check to make sure we can connect to the database
    try:
        db = SessionLocal()
        logger.info("Database connection established successfully.")
        
        # Check if there are any admin users
        admin_exists = db.query(User).filter(User.is_admin == True).first() is not None
        if not admin_exists:
            logger.info("No admin user found. Creating initial admin...")
            create_initial_admin(db)
            logger.info("Initial admin user created.")
        
        db.close()
        logger.info("Database connection closed.")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def create_initial_admin(db: Session):
    """Create the initial admin user if none exists."""
    hashed_password = get_password_hash("admin123")
    admin_user = User(
        email="admin@codance.com",
        username="admin",
        hashed_password=hashed_password,
        is_active=True,
        is_admin=True
    )
    db.add(admin_user)
    db.commit()

def create_sample_events(db: Session):
    """Create sample events."""
    now = datetime.utcnow()
    
    # Past event
    past_event = Event(
        name="Neuromorphic Resonance Alpha Test",
        description="Initial alpha test of the Neuromorphic Resonance system with a small group of dancers.",
        location="Studio 42, Amsterdam",
        start_time=now - timedelta(days=30),
        end_time=now - timedelta(days=30, hours=-4),
        is_active=False,
        max_capacity=20,
        configuration={
            "sound_intensity": 0.7,
            "visualization_intensity": 0.8,
            "haptic_feedback_enabled": True
        }
    )
    
    # Current event
    current_event = Event(
        name="Neuromorphic Resonance Beta Experience",
        description="Public beta test of the Neuromorphic Resonance system with expanded capabilities.",
        location="Warehouse 21, Berlin",
        start_time=now - timedelta(hours=2),
        end_time=now + timedelta(hours=6),
        is_active=True,
        max_capacity=100,
        configuration={
            "sound_intensity": 0.8,
            "visualization_intensity": 0.9,
            "haptic_feedback_enabled": True,
            "biometric_integration_enabled": True
        }
    )
    
    # Future event
    future_event = Event(
        name="Neuromorphic Resonance Festival Launch",
        description="Official launch of the Neuromorphic Resonance system at a major electronic music festival.",
        location="Techno Park, Barcelona",
        start_time=now + timedelta(days=30),
        end_time=now + timedelta(days=32),
        is_active=False,
        max_capacity=1000,
        configuration={
            "sound_intensity": 1.0,
            "visualization_intensity": 1.0,
            "haptic_feedback_enabled": True,
            "biometric_integration_enabled": True,
            "multi_zone_enabled": True
        }
    )
    
    db.add_all([past_event, current_event, future_event])
    db.commit()
    logger.info("Sample events created")

def create_sample_movement_patterns(db: Session):
    """Create sample movement patterns."""
    patterns = [
        MovementPattern(
            name="Wave",
            description="A wave-like movement pattern across the dance floor",
            pattern_data={
                "type": "wave",
                "direction": "horizontal",
                "frequency": 0.5,
                "amplitude": 0.8
            }
        ),
        MovementPattern(
            name="Spiral",
            description="A spiral movement pattern from the center outwards",
            pattern_data={
                "type": "spiral",
                "direction": "outward",
                "rotation_speed": 0.3,
                "expansion_rate": 0.2
            }
        ),
        MovementPattern(
            name="Pulse",
            description="A pulsing movement pattern where dancers move in and out from the center",
            pattern_data={
                "type": "pulse",
                "frequency": 0.25,
                "min_radius": 0.2,
                "max_radius": 0.9
            }
        ),
        MovementPattern(
            name="Split",
            description="A pattern where the dance floor splits into two distinct groups",
            pattern_data={
                "type": "split",
                "axis": "vertical",
                "separation_distance": 0.6,
                "group_cohesion": 0.8
            }
        )
    ]
    
    db.add_all(patterns)
    db.commit()
    logger.info("Sample movement patterns created")

def create_sample_sound_presets(db: Session):
    """Create sample sound presets."""
    presets = [
        SoundPreset(
            name="Deep Bass",
            description="A deep, resonant bass sound with long sustain",
            parameters={
                "waveform": "sine",
                "frequency_range": [30, 80],
                "envelope": {
                    "attack": 0.1,
                    "decay": 0.2,
                    "sustain": 0.8,
                    "release": 1.5
                },
                "filter": {
                    "type": "lowpass",
                    "cutoff": 200,
                    "resonance": 0.7
                }
            }
        ),
        SoundPreset(
            name="Techno Kick",
            description="A punchy techno kick drum sound",
            parameters={
                "type": "percussion",
                "subtype": "kick",
                "pitch": 0.8,
                "decay": 0.4,
                "click": 0.3,
                "body": 0.7,
                "filter": {
                    "type": "bandpass",
                    "cutoff": 120,
                    "resonance": 0.4
                }
            }
        ),
        SoundPreset(
            name="Ambient Pad",
            description="A spacious, evolving ambient pad sound",
            parameters={
                "waveform": "sawtooth",
                "voices": 4,
                "detune": 0.1,
                "frequency_range": [200, 2000],
                "envelope": {
                    "attack": 2.0,
                    "decay": 1.0,
                    "sustain": 0.7,
                    "release": 3.0
                },
                "modulation": {
                    "type": "lfo",
                    "target": "filter",
                    "rate": 0.2,
                    "depth": 0.3
                }
            }
        ),
        SoundPreset(
            name="Glitch Percussion",
            description="Glitchy, digital percussion sounds",
            parameters={
                "type": "percussion",
                "subtype": "glitch",
                "density": 0.7,
                "complexity": 0.8,
                "pitch_range": [0.5, 2.0],
                "filter": {
                    "type": "highpass",
                    "cutoff": 1000,
                    "resonance": 0.6
                }
            }
        )
    ]
    
    db.add_all(presets)
    db.commit()
    logger.info("Sample sound presets created")

def create_sample_visualization_presets(db: Session):
    """Create sample visualization presets."""
    presets = [
        VisualizationPreset(
            name="Geometric Pulse",
            description="Pulsing geometric shapes that react to the beat",
            parameters={
                "type": "holographic",
                "shapes": ["cube", "sphere", "pyramid"],
                "color_scheme": "complementary",
                "base_color": {
                    "hue": 240,
                    "saturation": 0.8,
                    "brightness": 0.9
                },
                "pulse_rate": 0.5,
                "rotation_speed": 0.2
            }
        ),
        VisualizationPreset(
            name="Fluid Waves",
            description="Fluid, wave-like visualizations that flow across the space",
            parameters={
                "type": "projection",
                "style": "fluid",
                "color_scheme": "analogous",
                "base_color": {
                    "hue": 180,
                    "saturation": 0.7,
                    "brightness": 0.8
                },
                "flow_speed": 0.3,
                "turbulence": 0.4,
                "resolution": "1080p"
            }
        ),
        VisualizationPreset(
            name="Particle Field",
            description="A field of particles that react to movement",
            parameters={
                "type": "holographic",
                "style": "particle",
                "particle_count": 10000,
                "particle_size": 0.02,
                "color_scheme": "monochrome",
                "base_color": {
                    "hue": 120,
                    "saturation": 0.5,
                    "brightness": 0.9
                },
                "reactivity": 0.8,
                "persistence": 0.3
            }
        ),
        VisualizationPreset(
            name="Laser Grid",
            description="A grid of laser beams that create geometric patterns",
            parameters={
                "type": "laser",
                "pattern": "grid",
                "density": 0.5,
                "color_scheme": "triadic",
                "base_color": {
                    "hue": 0,
                    "saturation": 1.0,
                    "brightness": 1.0
                },
                "movement_speed": 0.4,
                "beam_width": 0.02
            }
        )
    ]
    
    db.add_all(presets)
    db.commit()
    logger.info("Sample visualization presets created")

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization completed.") 