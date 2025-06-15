from app import models
from app.schemas import CreateAssistant, CreateChat, CreateMessage, MessageOut
from sqlalchemy.orm import Session
from app import gemini
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def create_assistant(db:Session, assistant:CreateAssistant) -> models.Assistant:
    """
    This function create a new assistant in the database.
    params:
        db (Session): The database session to use for the operation.
        assistant (CreateAssistant): The assistant data to be created.
    returns:
        models.Assistant: The created assistant object from the database.
    """
    try:
        assistant_db = models.Assistant(
            name = assistant.name,
            instructions = assistant.instructions
        )
        # Add the assistant to the session and commit to save it in the database
        db.add(assistant_db)
        db.commit()
        db.refresh(assistant_db)
        logger.info(f"Assistant created with ID: {assistant_db.id}")
        return assistant_db
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create assistant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create assistant: {str(e)}")
    
def get_assistant(db: Session, assistant_id: int) -> models.Assistant | None:
    """
    This function retrieves an assistant from the database by its ID.
    params:
        db (Session): The database session to use for the operation.
        assistant_id (int): The ID of the assistant to retrieve.
    returns:
        models.Assistant | None: The assistant object if found, otherwise None.
    """
    try:
        result =  db.query(models.Assistant).filter(models.Assistant.id == assistant_id).first()
        if not result:
            logger.warning(f"Assistant with ID {assistant_id} not found")
            raise HTTPException(status_code=404, detail="Assistant not found")
        return result
    except HTTPException:
        # Re raise the HTTPException if it was raised in the try block
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve assistant with ID {assistant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve assistant: {str(e)}")

def create_chat(db: Session, chat:CreateChat) -> models.Chat:
    """
    This function create a new chat in the data base.
    params:
        db (Session): The database session to use for the operation.
        chat (CreateChat): The chat data to be created.
    returns:
        models.Chat: The created chat object from the database.
    """
    try:
        result = db.query(models.Assistant).filter(models.Assistant.id == chat.assistant_id).first()
        if not result:
            logger.warning(f"Assistant with ID {chat.assistant_id} not found")
            raise HTTPException(status_code=404, detail="Assistant not found")
        chat_db = models.Chat(
            assistant_id = chat.assistant_id
        )
        db.add(chat_db)
        db.commit()
        db.refresh(chat_db)
        return chat_db
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create chat: {str(e)}")

def get_chat(db: Session, chat_id: int) -> models.Chat | None:
    """
    This function retrieves a chat from the database by its ID.
    params:
        db (Session): The database session to use for the operation.
        chat_id (int): The ID of the chat to retrieve.
    returns:
        models.Chat | None: The chat object if found, otherwise None.
    """
    try:
        result =  db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        if not result:
            logger.warning(f"Chat with ID {chat_id} not found")
            raise HTTPException(status_code=404, detail="Chat not found")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve chat with ID {chat_id}: {str(e)}")
        raise HTTPException(status_code=500,detail= f"Failed to retrieve chat: {str(e)}")
    
def get_chats(db:Session,skip:int=0, limit:int=10) -> list[models.Chat] | None :
    """
    This function retrieves all chats from the database.
    params:
        db (Session): The database session to use for the operation.
    returns:
        list[models.Chat] | None: A list of chat objects if found, otherwise None.
    """
    try:
        # Get the 'limit' newest (creation time) chats
        result = (
            db.query(models.Chat)
            .order_by(models.Chat.when_created.desc())
            .offset(skip)
            .limit(limit)
            .all()
            )
        if not result:
            logger.warning("No chats found in the database")
            raise HTTPException(status_code=404, detail="No chats found")
        return result
    except Exception as e:
        logger.error(f"Failed to retrieve chats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chats: {str(e)}")

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
        # Add the user message to the session and commit to save it in the database
        db.add(user_message_db)
        db.commit()
        db.refresh(user_message_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save user message: {str(e)}")

    # Get chat to retrieve system instructions from the assistant.
    chat = db.query(models.Chat).filter(models.Chat.id == message.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        system_instructions = chat.assistant.instructions
        user_input = message.content
        logger.info("Calling Gemini with system instructions and user input")
        gemini_response = gemini.get_gemini_resposne(system_instructions, user_input)
        logger.info("Gemini response received successfully")
    except Exception as e:
        logger.error(f"Failed to generate assistant response: {str(e)}")
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

def get_messages(db:Session, chat_id: int,skip:int=0, limit:int=10) -> list[models.Message]:
    """
    This function retrieves all messages from a chat in the database.
    params:
        db (Session): The database session to use for the operation.
        chat_id (int): The ID of the chat to retrieve messages from.
    returns:
        list[MessageOut]: A list of message objects from the database.
    """
    try:
        # Get the 'limit' messages in chat (chat id) oldest to newest
        messages = (
            db.query(models.Message)
            .filter(models.Message.chat_id == chat_id)
            .order_by(models.Message.message_sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
            )
        if not messages:
            logger.warning(f"No messages found for chat ID {chat_id}")
            raise HTTPException(status_code=404, detail="No messages found for this chat")
        messages.reverse()
        return [MessageOut.model_validate(message) for message in messages]
    except HTTPException:
        # Re-raise the HTTPException if it was raised in the try block
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve messages for chat {chat_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve messages: {str(e)}")