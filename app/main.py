from app import database,models
from fastapi import FastAPI, Depends
from app.routers import assistants, chats, messages
from google import genai




# Initialize the fastapi app
app = FastAPI()

# Include the routers for different endpoints
app.include_router(assistants.router, prefix="/assistants", tags=["assistants"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
# Creating the DB based on the models inherented the Base class
models.Base.metadata.create_all(bind=database.engine)



