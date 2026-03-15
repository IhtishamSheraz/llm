def decide_policy(is_injection, entities):

    # Injection detected
    if is_injection:
        return "BLOCK"

    # PII detected
    if entities:
        return "MASK"

    # Safe prompt
    return "ALLOW"