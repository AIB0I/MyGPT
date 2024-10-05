from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
import traceback

from .session import Session
from .db import DB
from .utils import logger

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize model settings
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_api_base = os.getenv("OLLAMA_API_BASE")

# Database dependency
def get_db():
    db = DB(os.getenv("APP_DB"))
    try:
        yield db
    finally:
        db.close()

class SessionMessage(BaseModel):
    """
    Pydantic model for session messages.
    """
    message: str
    session_id: str = None

@app.post("/session")
async def session(session_message: SessionMessage, db: DB = Depends(get_db)):
    """
    Handle a session message, creating a new session if necessary.

    Args:
        session_message (SessionMessage): The message and optional session ID.

    Returns:
        dict: A dictionary containing the AI's response and the session ID.

    Raises:
        HTTPException: If there's an error processing the message or if the session ID is invalid.
    """
    try:
        if not session_message.session_id:
            # Create a new session if no session ID is provided
            session_message.session_id = str(uuid.uuid4())
            db.add_session(session_message.session_id, "Temp Title")
            logger.info(f"Initiated new session with ID: {session_message.session_id}")
        else:
            # Validate if the provided session ID exists in the database
            if not db.check_session(session_message.session_id):
                logger.warning(f"Invalid session ID provided: {session_message.session_id}")
                raise HTTPException(status_code=404, detail="Invalid session ID")
            logger.info(f"Continuing session with ID: {session_message.session_id}")

        # Process the message and get the AI's response
        session = Session(ollama_model, ollama_api_base, db, session_message.session_id)
        response = session.add_message(session_message.message)
        logger.info(f"Sending response to user")
        return {"response": response, "session_id": session_message.session_id}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in session endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str, db: DB = Depends(get_db)):
    """
    Retrieve the message history for a given session.

    Args:
        session_id (str): The ID of the session to retrieve history for.

    Returns:
        dict: A dictionary containing the session ID and message history.

    Raises:
        HTTPException: If there's an error retrieving the session history.
    """
    try:
        history = db.get_session_history(session_id)
        return {"session_id": session_id, "history": history}
    
    except Exception as e:
        logger.error(f"Error retrieving session history: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Remove the global db instance and the shutdown event