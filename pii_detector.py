# pii_detector.py
import time
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

# ═══════════════════════════════════════════
# Customization 1: Pakistani Phone Recognizer
# ═══════════════════════════════════════════
pk_phone_recognizer = PatternRecognizer(
    supported_entity="PK_PHONE_NUMBER",
    patterns=[
        Pattern(
            name="PK_PHONE",
            regex=r"\b((\+92|0092|0)?3[0-9]{2}[\s\-]?[0-9]{7})\b",
            score=0.85
        )
    ],
    context=["phone", "call", "contact", "number", "mobile"]
)

# ═══════════════════════════════════════════
# Customization 2: API Key Recognizer
# ═══════════════════════════════════════════
api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern(
            name="GEMINI_KEY",
            regex=r"AIza[0-9A-Za-z\-_]{35}",
            score=0.95
        ),
        Pattern(
            name="OPENAI_KEY",
            regex=r"sk-[a-zA-Z0-9]{32,}",
            score=0.95
        ),
        Pattern(
            name="GENERIC_API_KEY",
            regex=r"\b[Aa][Pp][Ii][\s_-]?[Kk][Ee][Yy][\s:=]+[A-Za-z0-9\-_]{16,}\b",
            score=0.80
        )
    ],
    context=["api", "key", "token", "secret", "authorization"]
)

# ═══════════════════════════════════════════
# Customization 3: Pakistani CNIC Recognizer
# ═══════════════════════════════════════════
cnic_recognizer = PatternRecognizer(
    supported_entity="PK_CNIC",
    patterns=[
        Pattern(
            name="CNIC_FORMAT",
            regex=r"\b\d{5}-\d{7}-\d{1}\b",
            score=0.92
        )
    ],
    context=["cnic", "id", "identity", "national", "card"]
)

# ═══════════════════════════════════════════
# Setup Analyzer Engine
# ═══════════════════════════════════════════
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
}
provider    = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine  = provider.create_engine()

analyzer  = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

# Custom recognizers add karo
analyzer.registry.add_recognizer(pk_phone_recognizer)
analyzer.registry.add_recognizer(api_key_recognizer)
analyzer.registry.add_recognizer(cnic_recognizer)


# ═══════════════════════════════════════════
# Main Function
# ═══════════════════════════════════════════
def analyze_pii(text: str) -> dict:
    start = time.time()

    # Analyze karo
    results = analyzer.analyze(
        text=text,
        language="en"
    )

    IGNORE_ENTITIES = {"LOCATION", "DATE_TIME", "ORGANIZATION"}
    results = [
     r for r in results 
     if r.score >= 0.6 and r.entity_type not in IGNORE_ENTITIES
    ]
    # Anonymize (mask) karo
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    entities = [
        {
            "entity_type" : r.entity_type,
            "score"       : round(r.score, 2),
            "original"    : text[r.start:r.end]
        }
        for r in results
    ]

    latency_ms = round((time.time() - start) * 1000, 2)

    return {
        "original_text"  : text,
        "anonymized_text": anonymized.text,
        "entities_found" : entities,
        "pii_detected"   : len(results) > 0,
        "latency_ms"     : latency_ms
    }


# ═══════════════════════════════════════════
# Quick Test
# ═══════════════════════════════════════════
if __name__ == "__main__":
    tests = [
        "My phone number is 0312-3456789",
        "My CNIC is 35202-1234567-1",
        "API key is AIzaSyA9kbL1yXfY6jjrpdjS4BwRYk_cmrBp-LA",
        "My email is ali@gmail.com",
        "What is the capital of France?",
    ]

    for t in tests:
        print(f"\n{'='*50}")
        result = analyze_pii(t)
        print(f"Input     : {result['original_text']}")
        print(f"Masked    : {result['anonymized_text']}")
        print(f"Entities  : {result['entities_found']}")
        print(f"PII Found : {result['pii_detected']}")
        print(f"Latency   : {result['latency_ms']} ms")