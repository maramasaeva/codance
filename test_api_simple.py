import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Codance API Test",
    description="Simple test for the Codance API",
    version="0.1.0"
)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic information about the Codance API test.
    """
    return {
        "message": "Codance API Test Server",
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running correctly.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting simple test API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 