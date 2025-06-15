import pytest
from unittest.mock import patch, MagicMock
from app.gemini import get_gemini_response

@patch("app.gemini.client.models.generate_content")
def test_get_gemini_response(mock_generate_content):
    # Arrange
    mock_response = MagicMock()
    mock_response.text = "gemini mocked response"
    mock_generate_content.return_value = mock_response

    # Act
    user_input = "what is the most popular sport in the world?"
    system_instructions = "you are a sport assistant"

    result = get_gemini_response(system_instructions=system_instructions, user_input=user_input)

    # Assert
    assert isinstance(result,str)
    assert result == "gemini mocked response"
    mock_generate_content.assert_called_once()

