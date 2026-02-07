# AdvisoryAI – Template Intelligence MVP

## Problem
Financial advisory firms use Word templates that take hours to configure
for AI-based report generation. Identifying which sections can be safely
generated without breaking formatting or compliance is manual and slow.

## Solution
This project demonstrates a working MVP that:
- Accepts a firm-approved Word template
- Identifies narrative sections
- Uses an LLM to generate client-specific narrative
- Injects content without breaking formatting
- Outputs a client-ready Word document

## Tech Stack
- Python
- Streamlit
- python-docx
- Mock LLM (easily replaceable with Gemini/OpenAI)

## Setup Instructions
```bash
pip install -r requirements.txt
streamlit run app.py
