from dotenv import load_dotenv
import os
import openai

load_dotenv()  # load environment variables from .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)
