import os

from google import genai

from dotenv import load_dotenv

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("API_KEY"),
)