"""
This module is responsible for the functionality if interacting with the Google Gemini API.
It integrates the the gemini llm to generate responses based on user input and system instructions.
It does that by initilizing the Google genai client with the API key.
"""
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
# Initialize the Google genai client
client = genai.Client(api_key=api_key)

def get_gemini_response(system_instructions: str, user_input: str) -> str:
    """
    This function generates a response using the Gemini model.
    It uses the Google GenAI client to interact with the Gemini API.
    """
    # Example of generating content with the Gemini model
    # You can customize the parameters as needed
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        config = types.GenerateContentConfig(
            system_instruction = system_instructions),
            contents = [user_input]
    )
    return response.text

