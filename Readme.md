# AdvisoryAI – Template Intelligence MVP

## Overview
Financial advisory firms rely on compliance-approved Word templates to generate client reports.  
Configuring these templates for AI-driven generation is currently manual, slow, and error-prone—especially when formatting, tables, and regulatory language must remain unchanged.

This MVP demonstrates a **safe, scalable approach to automated template intelligence**.

---

## Problem Statement
- Firms onboard with **dozens of Word templates**
- Engineers manually decide which sections can be AI-generated
- Naive LLM usage breaks formatting, tables, or compliance text
- Each template takes hours to configure and does not scale

---

## Solution
This project implements a working MVP that:

- Accepts firm-approved Word templates (`.docx`)
- Analyses document structure automatically
- Identifies:
  - **Narrative sections** (safe for AI generation)
  - **Static sections** (compliance, disclosures, tables)
- Uses an LLM only for narrative content generation
- Injects content without modifying formatting or layout
- Outputs a clean, client-ready Word document

---

## How It Works
1. Upload a Word template  
2. Parse headings and section structure  
3. Classify each section as narrative or static  
4. Generate narrative text using client context  
5. Inject text into existing paragraphs only  
6. Download the final Word document  

Formatting, tables, and compliance text remain untouched.

---

## Key Design Principles
- **Structure before generation**
- **Conservative by default**
- **LLMs do not touch formatting**
- **Explainable section-level decisions**
- **Compliance-safe fallbacks**

---

## Tech Stack
- Python  
- Streamlit (UI + demo hosting)  
- python-docx (Word document parsing and injection)  
- LLM Interface (mocked, easily replaceable with Gemini or OpenAI)

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
