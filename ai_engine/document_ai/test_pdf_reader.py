
from .pdf_reader import extract_pdf


pdf_path = input("Enter PDF path: ").strip().strip('"')

try:
    data = extract_pdf(pdf_path)

    print("\n========== EXTRACTION REPORT ==========")
    print("Filename:", data["filename"])
    print("Total pages:", data["total_pages"])

    total_chars = 0
    ocr_pages = 0

    for page in data["pages"]:

        total_chars += page["character_count"]

        if page["extraction_method"] == "ocr":
            ocr_pages += 1

        print(
            f"Page {page['page_number']} | "
            f"Characters: {page['character_count']} | "
            f"Method: {page['extraction_method']}"
        )

    print("\n========== SUMMARY ==========")
    print("Total extracted characters:", total_chars)
    print("Pages processed with OCR:", ocr_pages)
    print("Pages processed natively:", data["total_pages"] - ocr_pages)

    if data["pages"]:
        print("\n========== FIRST PAGE PREVIEW ==========")
        print(data["pages"][0]["text"][:1500])

except Exception as error:
    print("Extraction failed:", error)
