from llm import classify_section_with_llm

# Hard safety keywords — NEVER generate these
STATIC_KEYWORDS = [
    "charges", "costs", "fees",
    "important information", "disclosure",
    "declaration", "terms", "conditions",
    "signature", "regulatory", "complaint",
    "appendix"
]

# Narrative bias hints (domain-aware)
NARRATIVE_HINTS = [
    "objective", "background", "overview",
    "suitability", "review", "recommendation",
    "strategy", "profile", "circumstances"
]


def is_static_by_rule(title: str) -> bool:
    title_lower = title.lower()
    return any(k in title_lower for k in STATIC_KEYWORDS)


def is_narrative_section(title: str, content: str) -> bool:
    """
    Decide whether a section should be AI-generated.

    Inputs:
    - title: section heading
    - content: plain text snippet (string)

    Returns:
    - True if narrative
    - False if static
    """

    title_lower = title.lower()

    # 1️⃣ Absolute safety: never touch compliance sections
    if is_static_by_rule(title):
        return False

    # 2️⃣ Strong narrative bias based on domain hints
    if any(hint in title_lower for hint in NARRATIVE_HINTS):
        return True

    # 3️⃣ If there is almost no text, treat as static
    if not content or len(content.strip()) < 40:
        return False

    # 4️⃣ Let LLM decide intent
    decision = classify_section_with_llm(
        section_title=title,
        section_content=content[:1500]
    )

    return decision == "NARRATIVE"
