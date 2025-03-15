from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import movement, biometrics, sound, users, events, visualization

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

# Include routers from different modules
app.include_router(movement.router, prefix="/api/v1/movement", tags=["Movement Tracking"])
app.include_router(biometrics.router, prefix="/api/v1/biometrics", tags=["Biometric Data"])
app.include_router(sound.router, prefix="/api/v1/sound", tags=["Sound Generation"])
app.include_router(users.router, prefix="/api/v1/users", tags=["User Management"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Event Management"])
app.include_router(visualization.router, prefix="/api/v1/visualization", tags=["Visualization"])

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 