# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("AIzaSyA9kbL1yXfY6jjrpdjS4BwRYk_cmrBp-LA")

# Injection Detection Thresholds
INJECTION_THRESHOLD_BLOCK = 0.7   # Score >= 0.7 = BLOCK
INJECTION_THRESHOLD_MASK  = 0.4   # Score >= 0.4 = MASK

# Presidio
PRESIDIO_CONFIDENCE = 0.6         # Minimum confidence for PII

# LLM Model
GEMINI_MODEL = "gemini-2.0-flash"