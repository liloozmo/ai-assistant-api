"""
This module imports the Pydantic `BaseModel` to define data models for request
 and response validation in an API layer. 
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Assistant creation input schema
class CreateAssistant(BaseModel):
    name: str
    instructions: str

# Assistant output schema
class AssistantOut(BaseModel):
    id: int
    name: str
    instructions: str

    model_config = ConfigDict(from_attributes=True)

# Chat creation input schema
class CreateChat(BaseModel):
    assistant_id: int

# Chat output schema
class ChatOut(BaseModel):
    id: int
    when_created: datetime
    assistant_id: int

    model_config = ConfigDict(from_attributes=True)

# Message creation input schema
class CreateMessage(BaseModel):
    content: str
    chat_id: int

# Message output schema
class MessageOut(BaseModel):
    writer: str
    content: str
    message_sent_at: datetime

    model_config = ConfigDict(from_attributes=True)