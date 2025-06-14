"""Test cases for the messages API endpoints."""
import pytest
from app.schemas import MessageOut
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

sample_input = {
    "content": "how are you?",
    "chat_id": 1
}
sample_output = {
    "writer": "assistant",
    "content": "i'm fine how about you?",
    "message_sent_at": "2023-10-01T12:00:00"
}

@pytest.fixture
def message_out():
    return MessageOut(**sample_output)
# Test for POST /messages/
@patch("app.routers.messages.crud.create_message")
def test_send_message(mocked_create_message, message_out):
    """
    Test the send_message endpoint for creating a new message.
    """
    # Arrange
    mocked_create_message.return_value = message_out
    # Act
    response = client.post("/messages/", json=sample_input)
    # Assert
    assert response.status_code == 200
    assert response.json() == sample_output
    mocked_create_message.assert_called_once()

# Test for GET /messages/{chat_id}/
@patch("app.routers.messages.crud.get_messages")
def test_get_messages(mocked_get_messages, message_out):
    """
    Test the get_messages endpoint for retrieving messages by chat ID.
    """
    # Arrange
    mocked_get_messages.return_value = [message_out]
    # Act
    response = client.get("/messages/1/")
    # Assert
    assert response.status_code == 200
    assert response.json() == [sample_output]
    mocked_get_messages.assert_called_once_with(chat_id=1, db=mocked_get_messages.call_args[1]["db"])

# Test for GET /messages/{chat_id}/ 
@patch("app.routers.messages.crud.get_messages")
def test_get_messages_empty(mocked_get_messages):
    """
    Test the get_messages endpoint when no messages exist for a chat ID.
    """
    # Arrange
    mocked_get_messages.return_value = []
    # Act
    response = client.get("/messages/1/")
    # Assert
    assert response.status_code == 200
    assert response.json() == []
    mocked_get_messages.assert_called_once_with(chat_id=1, db=mocked_get_messages.call_args[1]["db"])