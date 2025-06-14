"""
Test cases for CRUD operations
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from datetime import datetime

from app import crud, models, schemas


class TestCRUD:
    def test_create_assistant_success(self):
        """
        Test the creation of an assistant with valid data.
        """
        # Arrange
        db = MagicMock()
        assistant_data = schemas.CreateAssistant(name="hw assistant", instructions="Be helpful")

        # Act
        result = crud.create_assistant(db, assistant_data)

        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

        # Assert
        assert isinstance(result, models.Assistant)
        assert result.name == "hw assistant"

    def test_get_assistant_found(self):
        """
        Test retrieving an assistant by ID when it exists.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = models.Assistant(id=1, name="Test", instructions="Do stuff")

        # Act
        result = crud.get_assistant(db, 1)

        # Assert
        assert result.id == 1
        assert result.name == "Test"

    def test_get_assistant_not_found(self):
        """
        Test retrieving an assistant by ID when it does not exist.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            crud.get_assistant(db, 999)
        assert exc.value.status_code == 404

    def test_create_chat_success(self):
        """
        Test the creation of a chat with a valid assistant ID.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = models.Assistant(id=1, name="A", instructions="B")
        chat_data = schemas.CreateChat(assistant_id=1)

        # Act
        result = crud.create_chat(db, chat_data)

        # Assert
        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()
        assert isinstance(result, models.Chat)

    def test_get_chat_success(self):
        """
        Test retrieving a chat by ID when it exists.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = models.Chat(id=1, assistant_id=1)

        # Act
        result = crud.get_chat(db, 1)
        # Assert
        assert result.id == 1

    def test_get_chat_not_found(self):
        """
        Test retrieving a chat by ID when it does not exist.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = None
        # Act & Assert
        with pytest.raises(HTTPException):
            crud.get_chat(db, 404)

    def test_get_chats_success(self):
        """
        Test retrieving all chats when there are multiple chats.
        """
        # Arrange
        db = MagicMock()
        db.query().all.return_value = [models.Chat(id=1), models.Chat(id=2)]
        # Act
        result = crud.get_chats(db)
        # Assert
        assert len(result) == 2

    def test_get_chats_none(self):
        """
        Test retrieving all chats when there are no chats.
        """
        # Arrange
        db = MagicMock()
        db.query().all.return_value = []
        # Act & Assert
        with pytest.raises(HTTPException):
            crud.get_chats(db)

    @patch("app.crud.gemini.get_gemini_resposne", return_value="Hello user!")
    def test_create_message_success(self, mock_gemini):
        """
        Test the creation of a message with a valid chat ID and content.
        """
        # Arrange
        db = MagicMock()
        db.query().filter().first.return_value = models.Chat(
            id=1, assistant=models.Assistant(instructions="Be helpful")
        )
        message_data = schemas.CreateMessage(chat_id=1, content="Hi")
        # Act
        result = crud.create_message(db, message_data)
        # Assert
        db.add.assert_called()
        db.commit.assert_called()
        assert result.writer == "assistant"
        assert result.content == "Hello user!"

def test_get_messages_success():
    """
    Test retrieving messages for a chat when messages exist.
    """
    # Arrange
    db = MagicMock()
    db.query().filter().all.return_value = [
        models.Message(id=1, writer="user", chat_id=1, content="hi", message_sent_at=datetime(2025,1,1))
    ]
    # Act
    result = crud.get_messages(db, chat_id=1)
    # Assert
    assert isinstance(result, list)
    assert result[0].content == "hi"
    assert result[0].writer == "user"

def test_get_messages_none():
    """
    Test retrieving messages for a chat that has no messages.
    """
    # Arrange
    db = MagicMock()
    db.query().filter().all.return_value = []
    # Act & Assert

    with pytest.raises(HTTPException) as exc_info:
        crud.get_messages(db, chat_id=123)

    # Check if the status code is 404
    assert exc_info.value.status_code == 404



    