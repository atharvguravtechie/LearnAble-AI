
import os
import pymupdf

from .ocr_engine import extract_text_from_image


def extract_pdf(pdf_path):
    """
    Extract text from digital and scanned PDFs.
    Uses OCR when normal text extraction is insufficient.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = pymupdf.open(pdf_path)

    result = {
        "filename": os.path.basename(pdf_path),
        "total_pages": len(document),
        "pages": []
    }

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()
        method = "native"

        # Use OCR for pages with little or no extractable text
        if len(text) < 30:
            print(f"Running OCR on page {page_number}...")

            pix = page.get_pixmap(
                dpi=250,
                colorspace=pymupdf.csRGB,
                alpha=False
            )

            image_bytes = pix.tobytes("png")

            text = extract_text_from_image(image_bytes)
            method = "ocr"

        result["pages"].append({
            "page_number": page_number,
            "text": text,
            "character_count": len(text),
            "is_empty": len(text) == 0,
            "extraction_method": method
        })

    document.close()

    return result
