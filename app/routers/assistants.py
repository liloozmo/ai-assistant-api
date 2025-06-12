from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model = schemas.AssistantOut)
def create_assistant(
    assistant: schemas.CreateAssistant, db: Session = Depends(get_db)
) -> schemas.AssistantOut:
    """
    Post endpoint to create a new assistant.
    params:
        assistant (schemas.CreateAssistant): The assistant data to be created.
        db (Session): The database session to use for the operation.
    returns:
        schemas.AssistantOut: The created assistant object from the database.
    """
    # Return the created assistant object from the database
    return crud.create_assistant(db=db, assistant=assistant)

