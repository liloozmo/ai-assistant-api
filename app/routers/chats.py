from app import crud, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model = schemas.ChatOut)
def create_chat(chat: schemas.CreateChat, db:Session = Depends(get_db)) -> schemas.ChatOut:
    """
    Post endpoint to create a new chat.
    params:
        db (Session): The database session to use for the operation.
        chat (schemas.CreateChat): The chat data to be created.
    returns:
        schemas.ChatOut: The created chat object from the database.
    """
    # Return the created chat object from the database
    return crud.create_chat(db=db, chat=chat)