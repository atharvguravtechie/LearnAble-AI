
import json
import os

from .pdf_reader import extract_pdf
from .text_cleaner import clean_document


pdf_path = input("Enter PDF path: ").strip().strip('"')

try:
    print("\nExtracting PDF...")
    raw_document = extract_pdf(pdf_path)

    print("\nCleaning extracted content...")
    cleaned_document = clean_document(raw_document)

    # Ensure output directory exists
    os.makedirs("document_ai/output", exist_ok=True)

    output_path = "document_ai/output/cleaned_book.json"

    # Save structured output
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            cleaned_document,
            file,
            indent=4,
            ensure_ascii=False
        )

    total_raw = sum(
        page["raw_character_count"]
        for page in cleaned_document["pages"]
    )

    total_cleaned = sum(
        page["cleaned_character_count"]
        for page in cleaned_document["pages"]
    )

    print("\n========== CLEANING REPORT ==========")
    print("Filename:", cleaned_document["filename"])
    print("Total pages:", cleaned_document["total_pages"])
    print("Raw characters:", total_raw)
    print("Cleaned characters:", total_cleaned)

    print("\n========== FIRST PAGE PREVIEW ==========")

    if cleaned_document["pages"]:
        print(
            cleaned_document["pages"][0]["cleaned_text"][:2000]
        )

    print("\nSaved successfully:", output_path)

except Exception as error:
    print("\nProcessing failed:", error)
