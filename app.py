import streamlit as st
import json

from document_parser import parse_document
from section_classifier import is_narrative_section
from prompt_builder import build_prompt
from llm import generate_text
from injector import inject_generated_text

st.set_page_config(page_title="AdvisoryAI MVP", layout="wide")
st.title("Template → Client-Ready Word Report")

uploaded = st.file_uploader(
    "Upload Firm Template (.docx)",
    type=["docx"]
)

if uploaded:
    with open("client_context.json") as f:
        client = json.load(f)

    doc, sections = parse_document(uploaded)

    if st.button("Generate Client-Ready Report"):
        for section in sections:
            if is_narrative_section(section["title"]):
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

        with open(output_path, "rb") as f:
            st.download_button(
                "Download Generated Report",
                f,
                file_name="Generated_Suitability_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
