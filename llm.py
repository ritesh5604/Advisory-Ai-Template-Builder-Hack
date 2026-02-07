import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# ---------------------------------------------------------
# Gemini configuration (SAFE)
# ---------------------------------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not set. Please configure environment variables."
    )

genai.configure(api_key=API_KEY)

# Use FAST + CHEAP model for MVP
model = genai.GenerativeModel("gemini-2.5-pro")

# ---------------------------------------------------------
# Section classification (STRUCTURE ONLY)
# ---------------------------------------------------------
def classify_section_with_llm(section_title: str, section_content: str) -> str:
    prompt = f"""
You are classifying sections of financial documents.

Classify the section below as:
- NARRATIVE: client-specific written content
- STATIC: compliance, disclosures, tables, legal text

Respond with ONLY one word:
NARRATIVE or STATIC.

Section title:
{section_title}

Section content:
{section_content}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip().upper()

        if "NARRATIVE" in text:
            return "NARRATIVE"

        return "STATIC"

    except ResourceExhausted:
        # Conservative fallback (compliance-safe)
        return "STATIC"


# ---------------------------------------------------------
# Narrative generation (CONTENT ONLY)
# ---------------------------------------------------------
def generate_text(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except ResourceExhausted:
        return (
            "Based on the client’s circumstances and objectives, "
            "this section reflects a suitable approach aligned with "
            "their financial profile and long-term goals."
        )
print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))
