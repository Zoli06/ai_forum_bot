import os

from google import genai

gemini = genai.Client(
    api_key=os.environ['API_KEY']
)