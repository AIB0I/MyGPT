import uvicorn
import os

from .db import DB
from .api import app
from .utils import logger, log_file

def setup_db():
    db = DB(os.getenv("APP_DB"))
    db.create_tables()

if __name__ == "__main__":
    setup_db()
    logger.info(f"Starting the application, logging to: {log_file}")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
    )