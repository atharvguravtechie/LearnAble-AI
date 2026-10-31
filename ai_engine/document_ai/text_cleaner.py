
import re
import unicodedata


def clean_text(raw_text):
    """
    Clean extracted PDF/OCR text while preserving paragraphs.
    """

    if not raw_text:
        return ""

    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", raw_text)

    # Remove invisible soft hyphens
    text = text.replace("\u00ad", "")

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Fix words split across lines, e.g. computa-\ntion
    text = re.sub(
        r"(?<=\w)-[ \t]*\n[ \t]*(?=\w)",
        "",
        text
    )

    # Remove unnecessary spaces around lines
    lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(line)

    text = "\n".join(lines)

    # Limit excessive blank lines while preserving paragraphs
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces before punctuation
    text = re.sub(r"[ \t]+([.,;:!?])", r"\1", text)

    # Normalize repeated spaces
    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def clean_document(document_data):
    """
    Clean every page of an extracted document.
    Preserves the original OCR text.
    """

    cleaned_pages = []

    for page in document_data["pages"]:

        raw_text = page["text"]
        cleaned = clean_text(raw_text)

        cleaned_pages.append({
            "page_number": page["page_number"],
            "raw_text": raw_text,
            "cleaned_text": cleaned,
            "raw_character_count": len(raw_text),
            "cleaned_character_count": len(cleaned),
            "extraction_method": page["extraction_method"]
        })

    return {
        "filename": document_data["filename"],
        "total_pages": document_data["total_pages"],
        "pages": cleaned_pages
    }
