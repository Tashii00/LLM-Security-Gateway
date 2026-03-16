from config import BLOCK_SCORE, MASK_SCORE

def make_decision(injection_score, pii_detected):
    if injection_score >= BLOCK_SCORE:
        return {
            "decision": "BLOCK",
            "reason": f"High injection risk. Score: {injection_score}",
            "send_to_llm": False,
            "color": "🔴"
        }
    elif injection_score >= MASK_SCORE or pii_detected:
        reasons = []
        if pii_detected:
            reasons.append("PII detected")
        if injection_score >= MASK_SCORE:
            reasons.append(f"Medium injection risk (score: {injection_score})")
        return {
            "decision": "MASK",
            "reason": " + ".join(reasons),
            "send_to_llm": True,
            "color": "🟡"
        }
    else:
        return {
            "decision": "ALLOW",
            "reason": "Input is safe.",
            "send_to_llm": True,
            "color": "✅"
        }