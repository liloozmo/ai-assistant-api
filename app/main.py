from app import database,models
from fastapi import FastAPI, Depends

# Initialize the fastapi app
app = FastAPI()
# Creating the DB based on the models inherented the Base class
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.session_local()
    try:
        # 'yield' creats a single session for each reuqests
        yield db
    finally:
        db.close()

