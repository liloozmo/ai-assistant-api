from app import crud, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/",response_model= schemas.MessageOut)
def send_message(
    message:schemas.CreateMessage, 
    db: Session=Depends(get_db)
) -> schemas.MessageOut:
    """
    Post endpoint to send a message.
    params:
        message (schemas.CreateMessage): The message data to be sent.
        db (Session): The database session to use for the operation.
    returns:
        schemas.MessageOut: The sent message object from the database.
    """
    # Return the sent message object from the database
    return crud.create_message(db=db, message=message)

@router.get("/{chat_id}/", response_model= list[schemas.MessageOut])
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    limit: int= Query(10,ge=1,le=100),
    skip:int= Query(0,ge=0)) -> list[schemas.MessageOut]:
    """
    Get endpoint to retrieve messages by chat ID.
    params:
        chat_id (int): The ID of the chat to retrieve messages for.
        db (Session): The database session to use for the operation.
        limit (int): The number of messages to retrieve
        skip (int): The number of messages to skip (offset)
    returns:
        schemas.MessageOut: The message object if found, otherwise raises HTTPException.
    """
    return crud.get_messages(db=db, chat_id=chat_id,limit=limit,skip=skip)
    