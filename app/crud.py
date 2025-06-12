from app import models
from app.schemas import CreateAssistant, CreateChat, CreateMessage, MessageOut
from sqlalchemy.orm import Session
from app import gemini
from fastapi import HTTPException

def create_assistant(db:Session, assistant:CreateAssistant) -> models.Assistant:
    """
    This function create a new assistant in the database.
    params:
        db (Session): The database session to use for the operation.
        assistant (CreateAssistant): The assistant data to be created.
    returns:
        models.Assistant: The created assistant object from the database.
    """
    assistant_db = models.Assistant(
        name = assistant.name,
        instructions = assistant.instructions
    )
    db.add(assistant_db)
    db.commit()
    db.refresh(assistant_db)
    return assistant_db

def get_assistant(db: Session, assistant_id: int) -> models.Assistant | None:
    """
    This function retrieves an assistant from the database by its ID.
    params:
        db (Session): The database session to use for the operation.
        assistant_id (int): The ID of the assistant to retrieve.
    returns:
        models.Assistant | None: The assistant object if found, otherwise None.
    """
    return db.query(models.Assistant).filter(models.Assistant.id == assistant_id).first()

def create_chat(db: Session, chat:CreateChat) -> models.Chat:
    """
    This function create a new chat in the data base.
    params:
        db (Session): The database session to use for the operation.
        chat (CreateChat): The chat data to be created.
    returns:
        models.Chat: The created chat object from the database.
    """
    chat_db = models.Chat(
        assistant_id = chat.assistant_id
    )
    db.add(chat_db)
    db.commit()
    db.refresh(chat_db)
    return chat_db

def get_chat(db: Session, chat_id: int) -> models.Chat | None:
    """
    This function retrieves a chat from the database by its ID.
    params:
        db (Session): The database session to use for the operation.
        chat_id (int): The ID of the chat to retrieve.
    returns:
        models.Chat | None: The chat object if found, otherwise None.
    """
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def create_message(db: Session, message: CreateMessage, writer: str = "user") -> models.Message:
    """
    This function create a new message in the data base.
    params:
        db (Session): The database session to use for the operation.
        message (CreateMessage): The message data to be created.
        writer (str): The writer of the message.
    returns:
        models.Message: The created message object from the database.
    """
    try:
        # Save user message
        user_message_db = models.Message(
            content=message.content,
            chat_id=message.chat_id,
            writer=writer
        )
        db.add(user_message_db)
        db.commit()
        db.refresh(user_message_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save user message: {str(e)}")

    # Get chat and generate assistant response
    chat = db.query(models.Chat).filter(models.Chat.id == message.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        system_instructions = chat.assistant.instructions
        user_input = message.content
        gemini_response = gemini.get_gemini_resposne(system_instructions, user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate assistant response: {str(e)}")

    try:
        assistant_message_db = models.Message(
            content=gemini_response,
            chat_id=message.chat_id,
            writer="assistant"
        )
        db.add(assistant_message_db)
        db.commit()
        db.refresh(assistant_message_db)
        return assistant_message_db
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save assistant message: {str(e)}")

def get_messages(db:Session, chat_id: int) -> list[MessageOut]:
    """
    This function retrieves all messages from a chat in the database.
    params:
        db (Session): The database session to use for the operation.
        chat_id (int): The ID of the chat to retrieve messages from.
    returns:
        list[MessageOut]: A list of message objects from the database.
    """
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).all()