import os 
import pymupdf
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_path = r"D:\UNIT-I-DNC.pdf"

doc = pymupdf.open(pdf_path)

print("Total pages:", len(doc))

page = doc[0]

pix = page.get_pixmap(
    dpi=300,
    colorspace=pymupdf.csRGB,
    alpha=False
)

image = Image.frombytes(
    "RGB",
    [pix.width, pix.height],
    pix.samples
)

print("Image dimensions:", image.size)

os.makedirs("document_ai/output", exist_ok=True)

image.save("document_ai/output/test_page.png")

print("Page image saved successfully!")

text = pytesseract.image_to_string(
    image,
    lang="eng",
    config="--oem 3 --psm 3"
)

print("\n========== OCR RESULT ==========")
print(text[:3000])

print("\nCharacters detected:", len(text))

