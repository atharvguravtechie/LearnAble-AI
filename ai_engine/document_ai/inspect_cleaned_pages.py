
import json

INPUT_FILE = "document_ai/output/cleaned_book.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    document = json.load(file)

selected_pages = [1, 2, 3, 4, 6, 14, 20, 21, 27, 31, 34]

for page in document["pages"]:

    if page["page_number"] not in selected_pages:
        continue

    print("\n" + "=" * 65)
    print("PAGE:", page["page_number"])
    print("=" * 65)

    for number, line in enumerate(
        page["cleaned_text"].splitlines(), start=1
    ):
        if line.strip():
            print(f"{number:02d}. {line}")
