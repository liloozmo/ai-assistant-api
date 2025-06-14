"""
Test cases for the assistants API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.schemas import AssistantOut

client = TestClient(app)

# Sample data for testing
sample_input = {
    "name": "test assistant",
    "instructions": "you help with testing."
}

sample_output = {
    "id": 1,
    "name": "test assistant",
    "instructions": "you help with testing."
}


@pytest.fixture
def assistant_out():
    return AssistantOut(**sample_output)

# Test for POST /assistants/
@patch("app.routers.assistants.crud.create_assistant")
def test_create_assistant(mock_create_assistant, assistant_out):
    """
    Test the create_assistant endpoint for creating a new assistant.
    """
    mock_create_assistant.return_value = assistant_out

    response = client.post("/assistants/", json=sample_input)

    assert response.status_code == 200
    assert response.json() == sample_output
    mock_create_assistant.assert_called_once()

# Test for GET /assistants/{id}
@patch("app.routers.assistants.crud.get_assistant")
def test_get_assistant(mock_get_assistant, assistant_out):
    """ 
    Test the get_assistant endpoint for retrieving an assistant by ID.
    """
    mock_get_assistant.return_value = assistant_out

    response = client.get("/assistants/1/")

    assert response.status_code == 200
    assert response.json() == sample_output
    mock_get_assistant.assert_called_once_with(assistant_id=1, db=mock_get_assistant.call_args[1]['db'])
