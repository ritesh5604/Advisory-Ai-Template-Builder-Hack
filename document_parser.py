from docx import Document

def parse_document(docx_file):
    doc = Document(docx_file)
    sections = []

    current = None

    for para in doc.paragraphs:
        text = para.text.strip()
        style = para.style.name if para.style else ""

        if not text:
            continue

        if style.startswith("Heading"):
            current = {
                "title": text,
                "paragraphs": []
            }
            sections.append(current)
        else:
            if current:
                current["paragraphs"].append(para)

    return doc, sections
