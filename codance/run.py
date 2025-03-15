import uvicorn
import logging
from app.core.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Starting Codance API server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 