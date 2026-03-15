import re
from rapidfuzz import fuzz

# -----------------------------
# Injection patterns
# -----------------------------
INJECTION_PATTERNS = {
    "ignore previous instructions": 0.2,
    "disregard previous instructions": 0.2,
    "reveal system prompt": 0.3,
    "show system prompt": 0.3,
    "bypass safety": 0.3,
    "disable safety": 0.3,
    "jailbreak": 0.4,
    "override restrictions": 0.3,
    "developer mode": 0.3,
    "act as system": 0.2,
    "ignore all previous instructions": 0.3,
    "forget earlier instructions": 0.3,
    "print system prompt": 0.3,
    "display system prompt": 0.3,
    "leak system prompt": 0.4,
    "expose hidden prompt": 0.4,
    "tell me the system instructions": 0.3,
    "remove safety filters": 0.4,
    "disable content policy": 0.4,
    "enter jailbreak mode": 0.4,
    "act as developer": 0.3,
    "break the rules": 0.3,
    "ignore safety rules": 0.3,
    "override ai policy": 0.3,
    "simulate developer mode": 0.3
}

# Educational context words
EDUCATIONAL_CONTEXT = [
    "explain","research","study","paper","example","analysis",
    "learning","security","demonstrate","understand","education",
    "academic","assignment","project","investigate","discussion",
    "evaluation","method","approach","concept","theory","practice",
    "analysis of","explain why","case study"
]

THRESHOLD = 0.3

# Fuzzy similarity threshold
FUZZY_THRESHOLD = 80


def fuzzy_match(pattern, text):
    """
    Check fuzzy similarity between pattern and text
    """
    similarity = fuzz.partial_ratio(pattern, text)
    return similarity >= FUZZY_THRESHOLD


def detect_injection(prompt):

    text = prompt.lower()

    injection_score = 0
    context_score = 0

    # -----------------------------
    # Pattern detection
    # -----------------------------
    for pattern, weight in INJECTION_PATTERNS.items():

        # Exact regex match
        if re.search(pattern, text):
            injection_score += weight

        # Fuzzy match for typo detection
        elif fuzzy_match(pattern, text):
            injection_score += weight * 0.8  # slightly lower confidence

    # -----------------------------
    # Educational context check
    # -----------------------------
    for word in EDUCATIONAL_CONTEXT:
        if word in text:
            context_score += 0.2

    # -----------------------------
    # Final score
    # -----------------------------
    final_score = injection_score - context_score
    final_score = max(0, min(final_score, 1))

    is_attack = final_score >= THRESHOLD

    return is_attack, final_score