import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

BLOCK_SCORE = 0.7
MASK_SCORE = 0.4
MIN_CONFIDENCE = 0.6