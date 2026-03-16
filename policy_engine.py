# policy_engine.py

# Thresholds
BLOCK_THRESHOLD = 0.7
MASK_THRESHOLD  = 0.4

def make_decision(injection_score: float, pii_detected: bool) -> dict:

    # ── BLOCK: High injection risk ──
    if injection_score >= BLOCK_THRESHOLD:
        return {
            "decision"    : "BLOCK",
            "reason"      : f"High injection risk. Score: {injection_score}",
            "send_to_llm" : False,
            "color"       : "🔴"
        }

    # ── MASK: PII found ya medium injection risk ──
    elif injection_score >= MASK_THRESHOLD or pii_detected:
        reason = []
        if pii_detected:
            reason.append("PII detected")
        if injection_score >= MASK_THRESHOLD:
            reason.append(f"Medium injection risk (score: {injection_score})")
        return {
            "decision"    : "MASK",
            "reason"      : " + ".join(reason),
            "send_to_llm" : True,
            "color"       : "🟡"
        }

    # ── ALLOW: Sab safe hai ──
    else:
        return {
            "decision"    : "ALLOW",
            "reason"      : "Input is safe.",
            "send_to_llm" : True,
            "color"       : "✅"
        }


# ── Quick Test ──
if __name__ == "__main__":
    scenarios = [
        {"injection_score": 0.0,  "pii_detected": False, "label": "Normal query"},
        {"injection_score": 0.0,  "pii_detected": True,  "label": "PII in text"},
        {"injection_score": 0.45, "pii_detected": False, "label": "Medium injection"},
        {"injection_score": 0.75, "pii_detected": False, "label": "Jailbreak attempt"},
        {"injection_score": 0.80, "pii_detected": True,  "label": "Jailbreak + PII"},
    ]

    print(f"\n{'='*55}")
    print(f"{'Scenario':<25} {'Score':<8} {'PII':<6} {'Decision'}")
    print(f"{'='*55}")

    for s in scenarios:
        result = make_decision(s["injection_score"], s["pii_detected"])
        print(f"{s['label']:<25} {s['injection_score']:<8} "
              f"{str(s['pii_detected']):<6} "
              f"{result['color']} {result['decision']}")