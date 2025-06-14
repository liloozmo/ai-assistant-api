from app import database,models
from fastapi import FastAPI, Depends
from app.routers import assistants, chats, messages
from google import genai
import logging
from contextlib import asynccontextmanager


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up the application...")
    yield
    # Shutdown
    logger.info("Shutting down the application...")

# Initialize the fastapi app
app = FastAPI(lifespan=lifespan)


# Include the routers for different endpoints
app.include_router(assistants.router, prefix="/assistants", tags=["assistants"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
# Creating the DB based on the models inherented the Base class
models.Base.metadata.create_all(bind=database.engine)



