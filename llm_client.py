import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
USE_MOCK = True

mock_db = {
    "capital": "The capital of Pakistan is Islamabad.",
    "math":    "2 + 2 = 4",
    "weather": "I don't have real-time weather data.",
    "default": "This is a simulated LLM response for demonstration purposes.",
}

def get_mock(msg):
    m = msg.lower()
    if "capital" in m: return mock_db["capital"]
    if "2 + 2" in m:   return mock_db["math"]
    if "weather" in m: return mock_db["weather"]
    return mock_db["default"]

def call_llm(msg):
    if not USE_MOCK and API_KEY:
        try:
            import google.genai as genai
            c = genai.Client(api_key=API_KEY)
            r = c.models.generate_content(model="gemini-1.5-flash", contents=msg)
            return r.text
        except:
            return get_mock(msg)
    time.sleep(0.1)
    return get_mock(msg)