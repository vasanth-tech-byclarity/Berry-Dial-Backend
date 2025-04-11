import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
BASE_URL = os.getenv("BASE_URL")
HEADERS = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

# Database Configuration
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE")
}