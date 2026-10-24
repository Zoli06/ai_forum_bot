import os

from google import genai

from lemmy import lemmy

gemini = genai.Client(
    api_key=os.environ['API_KEY']
)