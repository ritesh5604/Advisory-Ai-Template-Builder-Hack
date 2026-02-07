NARRATIVE_KEYWORDS = [
    "suitability",
    "rationale",
    "objective",
    "strategy",
    "summary",
    "profile",
    "recommend"
]

BLOCKED_KEYWORDS = [
    "disclosure",
    "important",
    "charges",
    "fees",
    "table"
]

def is_narrative_section(title: str) -> bool:
    t = title.lower()

    if any(b in t for b in BLOCKED_KEYWORDS):
        return False

    return any(k in t for k in NARRATIVE_KEYWORDS)
