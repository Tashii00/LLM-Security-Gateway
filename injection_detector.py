import re
import time

patterns = [
    (r"ignore.{0,20}instructions", 0.30),
    (r"you are now", 0.20),
    (r"act as (dan|jailbreak|evil|unrestricted)", 0.35),
    (r"system prompt", 0.25),
    (r"forget (your|all) (rules|instructions)", 0.30),
    (r"bypass", 0.20),
    (r"jailbreak", 0.35),
    (r"do anything now", 0.30),
    (r"no restrictions", 0.25),
    (r"pretend (you are|to be)", 0.20),
    (r"disregard (all|your|previous)", 0.25),
    (r"you have no (rules|limits|restrictions)", 0.35),
    (r"override (your|all) (instructions|rules)", 0.35),
    (r"reveal (your|the) (system|prompt|key)", 0.30),
    (r"simulate (an? )?(evil|unrestricted|dan)", 0.35),
]

def detect_injection(text):
    t = time.time()
    lower = text.lower()
    score = 0.0
    found = []

    for p, w in patterns:
        if re.search(p, lower):
            score += w
            found.append(p)

    score = round(min(score, 1.0), 2)

    return {
        "injection_score": score,
        "matched_patterns": found,
        "is_suspicious": score >= 0.4,
        "latency_ms": round((time.time() - t) * 1000, 4)
    }