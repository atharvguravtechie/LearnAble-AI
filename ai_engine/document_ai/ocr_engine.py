
import io
import pytesseract

from PIL import Image


# Tesseract executable location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_bytes, language="eng"):
    """
    Extract text from a page image using Tesseract OCR.
    """

    image = Image.open(io.BytesIO(image_bytes))

    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    text = pytesseract.image_to_string(
        image,
        lang=language,
        config="--oem 3 --psm 3"
    )

    return text.strip()
