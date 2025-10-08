import os
import openai
from dotenv import load_dotenv

#  Load environment variables from .env file
load_dotenv()

#  Read the key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is not set in environment variables")

#  Initialize Groq Client
groq_client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)
