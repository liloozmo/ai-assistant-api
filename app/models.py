"""
Models for the application that defining the database schema using SQLAlchemy orm.
"""
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class Assistant(Base):
    __tablename__ = "assistants"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    instructions = Column(String,nullable=False)

    chats = relationship("Chat",back_populates="assistant")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer,primary_key=True)
    when_created = Column(DateTime,default=lambda:datetime.now(ZoneInfo("Asia/Jerusalem")))
    assistant_id = Column(Integer,ForeignKey("assistants.id"),nullable=False)

    assistant = relationship("Assistant",back_populates="chats")
    # Include 'delete-orphan' to ensure a message is deleted if it's removed from the chat's messages list
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan") 

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer,primary_key=True)
    writer = Column(String,nullable=False)
    chat_id = Column(Integer,ForeignKey("chats.id"),nullable=False) #check if not redundant
    content = Column(String,nullable=False)
    message_sent_at = Column(DateTime,default=lambda:datetime.now(ZoneInfo("Asia/Jerusalem")))

    chat = relationship("Chat",back_populates="messages")




