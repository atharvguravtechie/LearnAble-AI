
import json
import os

from .structure_detector import detect_document_structure


INPUT_FILE = "document_ai/output/cleaned_book.json"
OUTPUT_FILE = "document_ai/output/structured_book.json"


def main():

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(INPUT_FILE)

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        cleaned_document = json.load(file)

    print("Detecting document structure...")

    structured_document = detect_document_structure(
        cleaned_document
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            structured_document,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n========== STRUCTURE REPORT ==========")
    print("Document:", structured_document["filename"])
    print("Pages:", structured_document["total_pages"])
    print("Detected chapters:", structured_document["total_chapters"])

    for index, chapter in enumerate(
        structured_document["chapters"], start=1
    ):

        print(f"\n{index}. {chapter['title']}")
        print("   Page:", chapter["page_number"])
        print("   Sections:", len(chapter["sections"]))

        for section in chapter["sections"]:
            print(
                f"      - {section['title']} "
                f"(Page {section['page_number']})"
            )

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
