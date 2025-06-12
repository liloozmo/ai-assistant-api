"""
This module imports the Pydantic `BaseModel` to define data models for request and response validation
in an API layer. These models specify the structure and types of data expected as input to the API
and the format of data returned as output. By leveraging Pydantic's validation capabilities, this
module ensures that the data exchanged between the client and the API adheres to the defined schema,
helping to maintain data integrity and reduce errors.
"""
from pydantic import BaseModel
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

    class Config:
        # Enable ORM mode to read data from SQLAlchemy models
        orm_mode = True

# Chat creation input schema
class CreateChat(BaseModel):
    assistant_id: int

# Chat output schema
class ChatOut(BaseModel):
    id: int
    when_created: datetime
    assistant_id: int

    class Config:
        orm_mode = True

# Message creation input schema
class CreateMessage(BaseModel):
    content: str
    chat_id: int

# Message output schema
class MessageOut(BaseModel):
    writer: str
    content: str
    message_sent_at: datetime

    class Config:
        # Enable ORM mode to read data from SQLAlchemy models
        orm_mode = True  