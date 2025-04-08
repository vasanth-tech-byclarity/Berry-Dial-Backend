# ELEVENLABS_API_KEY = "sk_99887aa0f05b47d1b18e6d649c25d46a45b7a9ebe0dea8cb"
# OPENAI_API_KEY = "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"
# AGENT_ID = "VzOzId0oBDSRfpM9q1Pk"
# BASE_URL = "https://api.elevenlabs.io/v1/convai"
# HEADERS = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}


# # Database Configuration
# DB_CONFIG = {
#     'host': '15.207.173.143',
#     'user': 'appoinment',
#     'password': 'Appoinment456&',
#     'database': 'dental_appointments'
# }


import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# API Keys
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

# ElevenLabs API config
BASE_URL = "https://api.elevenlabs.io/v1/convai"
HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
