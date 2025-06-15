# Assistant Chat API
This project is a simplified version of OpenAI’s Assistant API built using FastAPI, SQLite, and Gemini API (from Google AI). It allows you to:

- Create Assistants with a name and system instructions
- Start chats with those Assistants
- Send messages and receive LLM generated responses
- Persist all data across restarts



###  Tech Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **Database**: SQLite (with SQLAlchemy ORM)
- **LLM**: Gemini API
- **migraations**: alembic
- **Testing**: pytest



### Project Structure:
```text
AI_ASISTANT_API/
│
├── alembic/                         
│   ├── versions/                  
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│
├── alembic.ini                 
│
├── app/   
│   ├── routers/                    
│   │   ├── __init__.py
│   │   ├── assistant.py
│   │   ├── chats.py
│   │   └── messages.py
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── gemini.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py                  
│
├── tests/                    
│   ├── __init__.py
│   ├── test_gemini.py
│   ├── test_crud.py
│   ├── test_assistants.py
│   ├── test_messages.py
│   └── test_chats.py
│
│
├── requirements.txt         
├── .env                      
├── README.md 

```

### How to run:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AI_ASSISTANT_API.git
cd ai-assistant-api

```
### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate

```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
alembic upgrade head
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```


### Running Tests

Run the tests with:
```bash
pytest tests/
```

This will test:
- Gemini integration 
- CRUD logic
- Assistant, chat, message flows



### Manual API Testing

Once the app is running you can manually test via:

### Swagger UI:
[http://localhost:8000/docs](http://localhost:8000/docs)


### Loom video
