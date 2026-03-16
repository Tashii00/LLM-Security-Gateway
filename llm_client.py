# llm_client.py
import os
import time
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("AIzaSyAt8x6q7Z8eyU7fGfMTX4EMdnKEuvypj2E")
USE_MOCK = True  # Real API available ho toh False karo

# ── Mock Responses (Demo ke liye) ──
MOCK_RESPONSES = {
    "default"   : "This is a simulated LLM response for demonstration purposes.",
    "capital"   : "The capital of Pakistan is Islamabad.",
    "math"      : "2 + 2 = 4",
    "weather"   : "I don't have real-time weather data.",
}

def get_mock_response(message: str) -> str:
    msg = message.lower()
    if "capital" in msg:
        return MOCK_RESPONSES["capital"]
    elif "2 + 2" in msg or "math" in msg:
        return MOCK_RESPONSES["math"]
    elif "weather" in msg:
        return MOCK_RESPONSES["weather"]
    else:
        return MOCK_RESPONSES["default"]

def call_llm(user_message: str) -> str:
    start = time.time()

    # ── Try Real API First ──
    if not USE_MOCK and GEMINI_API_KEY:
        try:
            import google.genai as genai
            client   = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model    = "gemini-1.5-flash",
                contents = user_message
            )
            latency = round((time.time() - start) * 1000, 2)
            return response.text

        except Exception as e:
            # Fallback to mock if API fails
            return get_mock_response(user_message)

    # ── Mock Mode ──
    time.sleep(0.1)  # Simulate latency
    return get_mock_response(user_message)


# ── Quick Test ──
if __name__ == "__main__":
    tests = [
        "What is 2 + 2?",
        "What is the capital of Pakistan?",
        "Tell me about AI security",
    ]

    for t in tests:
        print(f"\nQuestion : {t}")
        answer = call_llm(t)
        print(f"Answer   : {answer}")