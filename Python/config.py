# config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Force-load .env explicitly
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not loaded")

SESSION_TTL_SECONDS = 15 * 60
MIDAS_BASE_URL = "https://172.10.0.74:6001/services/midas"
VERIFY_SSL = False
