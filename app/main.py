from app import database,models
from fastapi import FastAPI, Depends
from app.routers import assistants, chats, messages
from google import genai
import logging
from contextlib import asynccontextmanager

# Initialize logging to use logger.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Define the lifespan of the app to handle startup and shutdown events.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up the application...")
    yield
    # Shutdown
    logger.info("Shutting down the application...")

# Initialize the fastapi app
app = FastAPI(lifespan=lifespan)


# Include the routers for different endpoints.
# Tags are used for grouping endpoints in the openapi documentation (like swagger).
app.include_router(assistants.router, prefix="/assistants", tags=["assistants"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
# Creating the DB based on the models inherented the Base class
models.Base.metadata.create_all(bind=database.engine)



