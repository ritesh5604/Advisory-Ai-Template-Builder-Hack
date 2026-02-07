import streamlit as st
import json

from document_parser import parse_document
from section_classifier import is_narrative_section
from prompt_builder import build_prompt
from llm import generate_text
from injector import inject_generated_text


# ---------------------------------------------------------
# Cache ONLY LLM decisions (safe + serializable)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def classify_section_decisions(section_signatures):
    """
    section_signatures: List of (title, text_snippet)
    returns: {title: is_narrative_bool}
    """
    decisions = {}
    for title, content in section_signatures:
        decisions[title] = is_narrative_section(title, content)
    return decisions


# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Template Intelligence",
    layout="centered"
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("Template Intelligence")
st.caption(
    "Turn firm-approved Word templates into client-ready reports. "
    "Narrative is generated automatically. Formatting stays untouched."
)

st.divider()

# ---------------------------------------------------------
# STEP 1 — Upload template
# ---------------------------------------------------------
st.header("Upload your Word template")
st.caption("Use the same compliance-approved template your firm already relies on.")

uploaded = st.file_uploader(
    "Upload .docx file",
    type=["docx"],
    label_visibility="collapsed"
)

if not uploaded:
    st.stop()

# ---------------------------------------------------------
# Parse document
# ---------------------------------------------------------
doc, sections = parse_document(uploaded)

# ---------------------------------------------------------
# STEP 2 — Build lightweight signatures for LLM
# ---------------------------------------------------------
section_signatures = []
for section in sections:
    snippet = " ".join(
        p.text for p in section["paragraphs"][:2] if p.text.strip()
    )
    section_signatures.append((section["title"], snippet))

# ---------------------------------------------------------
# STEP 3 — Classify sections (LLM runs HERE only)
# ---------------------------------------------------------
with st.spinner("Analysing template structure…"):
    narrative_map = classify_section_decisions(section_signatures)

st.divider()

# ---------------------------------------------------------
# STEP 4 — Show understanding
# ---------------------------------------------------------
st.header("Here’s what we found in your template")

left, right = st.columns(2)

with left:
    st.subheader("We will write here")
    for section in sections:
        if narrative_map.get(section["title"], False):
            st.write(f"🟢 {section['title']}")

with right:
    st.subheader("We will not touch these")
    for section in sections:
        if not narrative_map.get(section["title"], False):
            st.write(f"🔒 {section['title']}")

st.caption(
    "Only narrative sections are personalised. "
    "Tables, formatting, and compliance text remain unchanged."
)

st.divider()

# ---------------------------------------------------------
# STEP 5 — Client context (mock, explicit)
# ---------------------------------------------------------
st.header("Client this report is being generated for")

with open("client_context.json") as f:
    client = json.load(f)

with st.container(border=True):
    st.write(f"**Name:** {client['client_name']}")
    st.write(f"**Employment:** {client['employment']}")
    st.write(f"**Risk profile:** {client['risk_profile']}")
    st.write(f"**Objectives:** {', '.join(client['primary_objectives'])}")
    st.write(f"**Investment horizon:** {client['investment_horizon']}")

st.caption(
    "Client data already exists in AdvisoryAI systems. "
    "Shown here for demo purposes."
)

st.divider()

# ---------------------------------------------------------
# STEP 6 — Generate report
# ---------------------------------------------------------
generate = st.button(
    "Generate client-ready Word report",
    type="primary"
)

if not generate:
    st.stop()

# ---------------------------------------------------------
# Generation flow (NO LLM classification here)
# ---------------------------------------------------------
with st.spinner("Generating your report…"):
    for section in sections:
        if not narrative_map.get(section["title"], False):
            continue

        paragraphs = section["paragraphs"]
        if not paragraphs:
            continue

        original_text = paragraphs[0].text

        prompt = build_prompt(
            section["title"],
            client,
            original_text
        )

        generated_text = generate_text(prompt)
        inject_generated_text(paragraphs, generated_text)

    output_path = "Generated_Suitability_Report.docx"
    doc.save(output_path)

# ---------------------------------------------------------
# STEP 7 — Download
# ---------------------------------------------------------
st.success("Your report is ready.")

with open(output_path, "rb") as f:
    st.download_button(
        "Download Word document",
        f,
        file_name="Generated_Suitability_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.caption("Opens cleanly in Microsoft Word.")
