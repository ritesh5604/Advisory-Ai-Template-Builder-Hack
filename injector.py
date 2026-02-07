def inject_generated_text(paragraphs, new_text):
    """
    Replace ONLY the first meaningful paragraph
    to preserve structure and avoid duplication.
    """
    for para in paragraphs:
        if para.text.strip():   # first non-empty paragraph
            para.text = new_text
            break
