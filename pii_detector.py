import time
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

phone_rec = PatternRecognizer(
    supported_entity="PK_PHONE_NUMBER",
    patterns=[Pattern("PK_PHONE", r"\b((\+92|0092|0)?3[0-9]{2}[\s\-]?[0-9]{7})\b", 0.85)],
    context=["phone", "call", "contact", "number", "mobile"]
)

apikey_rec = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern("GEMINI", r"AIza[0-9A-Za-z\-_]{35}", 0.95),
        Pattern("OPENAI", r"sk-[a-zA-Z0-9]{32,}", 0.95),
    ],
    context=["api", "key", "token", "secret"]
)

cnic_rec = PatternRecognizer(
    supported_entity="PK_CNIC",
    patterns=[Pattern("CNIC", r"\b\d{5}-\d{7}-\d{1}\b", 0.92)],
    context=["cnic", "id", "identity", "national"]
)

cfg = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
}
nlp = NlpEngineProvider(nlp_configuration=cfg).create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp)
anonymizer = AnonymizerEngine()

analyzer.registry.add_recognizer(phone_rec)
analyzer.registry.add_recognizer(apikey_rec)
analyzer.registry.add_recognizer(cnic_rec)

IGNORE = {"LOCATION", "DATE_TIME", "ORGANIZATION"}

def analyze_pii(text):
    t = time.time()
    raw = analyzer.analyze(text=text, language="en")
    results = [r for r in raw if r.score >= 0.6 and r.entity_type not in IGNORE]
    anon = anonymizer.anonymize(text=text, analyzer_results=results)

    entities = [
        {"entity_type": r.entity_type, "score": round(r.score, 2), "original": text[r.start:r.end]}
        for r in results
    ]

    return {
        "original_text": text,
        "anonymized_text": anon.text,
        "entities_found": entities,
        "pii_detected": len(results) > 0,
        "latency_ms": round((time.time() - t) * 1000, 2)
    }