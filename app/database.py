from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
DATABASE_URL = "sqlite:///./app.db"
# Create engine to connect to the database. Ensure different users can use the same db connection.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory. Ensure manual commiting and pushing to DB for safer interaction 
session_local = sessionmaker(autocommit= False, autoflush=False, bind=engine)
