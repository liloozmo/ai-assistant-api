"""
Tests for the chat endpoints in the FastAPI application.
"""
import pytest
from app.schemas import ChatOut
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

sample_input = {
    "assistant_id": 1
}
sample_output = {
    "id": 1,
    "when_created": "2023-10-01T12:00:00",
    "assistant_id": 1
}

@pytest.fixture
def chat_out():
    return ChatOut(**sample_output)

# Test for POST /chats/
@patch("app.routers.chats.crud.create_chat")
def test_create_chat(mocked_create_chat, chat_out):
    """
    Test the create_chat endpoint for creating a new chat.
    """
    # Arrange
    mocked_create_chat.return_value = chat_out
    # Act
    response = client.post("/chats/", json= sample_input)
    # Assert
    assert response.status_code == 200
    assert response.json() == sample_output
    mocked_create_chat.assert_called_once()

#Test for GET /chats/{id}
@patch("app.routers.chats.crud.get_chat")
def test_get_chat(mocked_get_chat, chat_out):
    """ 
    Test the get_chat endpoint for retrieving a chat by ID.
    """
    # Arrange
    mocked_get_chat.return_value = chat_out
    # Act
    response = client.get("/chats/1")
    # Assert
    assert response.status_code == 200
    assert response.json() == sample_output
    mocked_get_chat.assert_called_once_with(chat_id = 1, db=mocked_get_chat.call_args[1]["db"])

# Test for GET /chats/
@patch("app.routers.chats.crud.get_chats")
def test_get_chats(mocked_get_chats, chat_out):
    """ 
    Test the get_chats endopoint for rerieving all chats.
    """
    # Arrange
    mocked_get_chats.return_value = [chat_out]
    # Act
    response = client.get("/chats/")
    # Assert
    assert response.status_code == 200
    assert response.json() == [sample_output]
    mocked_get_chats.assert_called_once_with(db=mocked_get_chats.call_args[1]["db"])
