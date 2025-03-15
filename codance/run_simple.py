import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting simplified Codance API server...")
    uvicorn.run("app.main_simple:app", host="0.0.0.0", port=8000, reload=True) 