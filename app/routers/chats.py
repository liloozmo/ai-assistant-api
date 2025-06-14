from app import crud, schemas
from app.database import get_db
from fastapi import APIRouter, Depends
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

@router.get("/{chat_id}", response_model=schemas.ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db)) -> schemas.ChatOut:
    """
    Get endpoint to retrieve a chat by its ID.
    params:
        chat_id (int): The ID of the chat to retrieve.
        db (Session): The database session to use for the operation.
    returns:
        schemas.ChatOut: The chat object if found, otherwise raises an HTTPException.
    """
    # Return the chat object from the database
    return crud.get_chat(db=db, chat_id=chat_id)

@router.get("/", response_model=list[schemas.ChatOut])
def get_chats(db: Session = Depends(get_db)) -> list[schemas.ChatOut]:
    """
    Get endpoint to retrieve all chats.
    params:
        db (Session): The database session to use for the operation.
    returns:
        list[models.Chat]: A list of all chat objects from the database.
    """
    # Return a list of all chat objects from the database
    return crud.get_chats(db=db)
