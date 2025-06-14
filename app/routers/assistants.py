from fastapi import APIRouter, Depends
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

@router.get("/{assistant_id}/", response_model=schemas.AssistantOut)
def get_assistant(
        assistant_id:int,
        db:Session = Depends(get_db)
) -> schemas.AssistantOut:
    """
    Get endpoint to retrieve an assistant by its ID.
    params:
        assistant_id (int): The ID of the assistant to retrieve.
        db (Session): The database session to use for the operation.
    returns:
        schemas.AssistantOut: The assistant object if found, otherwise raises HTTPException.
    """
    return crud.get_assistant(db=db, assistant_id=assistant_id)

