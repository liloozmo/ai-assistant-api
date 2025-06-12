from app import crud, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
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