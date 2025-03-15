from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Codance API",
    description="API for the Neuromorphic Resonance dance-driven AI ecosystem",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic information about the Codance API.
    """
    return {
        "message": "Welcome to the Codance API for Neuromorphic Resonance",
        "documentation": "/docs",
        "version": "0.1.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running correctly.
    """
    return {"status": "healthy"}

# User endpoints
@app.get("/api/v1/users", tags=["User Management"])
async def list_users():
    """
    List all users (placeholder).
    """
    return {"users": [{"id": 1, "username": "admin", "email": "admin@codance.com"}]}

@app.get("/api/v1/users/me", tags=["User Management"])
async def get_current_user():
    """
    Get current user information (placeholder).
    """
    return {"id": 1, "username": "admin", "email": "admin@codance.com"}

# Event endpoints
@app.get("/api/v1/events", tags=["Event Management"])
async def list_events():
    """
    List all events (placeholder).
    """
    return {"events": [{"id": 1, "name": "Neuromorphic Resonance Beta Experience", "location": "Berlin"}]}

# Movement endpoints
@app.get("/api/v1/movement/data", tags=["Movement Tracking"])
async def list_movement_data():
    """
    List movement data (placeholder).
    """
    return {"movement_data": [{"id": 1, "event_id": 1, "data_type": "heatmap"}]}

# Biometric endpoints
@app.get("/api/v1/biometrics/data", tags=["Biometric Data"])
async def list_biometric_data():
    """
    List biometric data (placeholder).
    """
    return {"biometric_data": [{"id": 1, "user_id": 1, "event_id": 1, "heart_rate": 75.5}]}

# Sound endpoints
@app.get("/api/v1/sound/events", tags=["Sound Generation"])
async def list_sound_events():
    """
    List sound events (placeholder).
    """
    return {"sound_events": [{"id": 1, "event_id": 1, "sound_type": "ambient"}]}

# Visualization endpoints
@app.get("/api/v1/visualization/events", tags=["Visualization"])
async def list_visualization_events():
    """
    List visualization events (placeholder).
    """
    return {"visualization_events": [{"id": 1, "event_id": 1, "visualization_type": "holographic"}]} 