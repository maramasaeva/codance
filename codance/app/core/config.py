import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Codance - Neuromorphic Resonance Platform"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./codance.db")
    
    # Sound Engine settings
    AUDIO_SAMPLE_RATE: int = 44100
    AUDIO_BUFFER_SIZE: int = 1024
    
    # Movement tracking settings
    CAMERA_FRAME_RATE: int = 30
    MOVEMENT_TRACKING_THRESHOLD: float = 0.1
    
    # Biometric data settings
    HEART_RATE_SAMPLING_RATE: int = 1  # Hz
    GSR_SAMPLING_RATE: int = 5  # Hz
    TEMPERATURE_SAMPLING_RATE: int = 1  # Hz
    
    # Visualization settings
    VISUALIZATION_FRAME_RATE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings() 