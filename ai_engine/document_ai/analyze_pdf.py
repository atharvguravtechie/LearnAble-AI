
import json
import os
import sys

from document_ai.pdf_reader import extract_pdf
from document_ai.text_cleaner import clean_document
from document_ai.structure_detector import detect_document_structure
from document_ai.semantic_analyzer import analyse_document
from document_ai.importance_ranker import rank_document


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def analyze_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        print("ERROR: PDF file not found:", pdf_path)
        return

    if not pdf_path.lower().endswith(".pdf"):
        print("ERROR: Please provide a PDF file.")
        return

    output_dir = os.path.join("document_ai", "output")
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(pdf_path)

    print("\n===================================")
    print(" UNIVERSAL INTELLIGENT PDF ANALYZER")
    print("===================================")
    print("Input:", filename)

    # Stage 1: Extraction and OCR
    print("\n[1/5] Extracting PDF text...")
    extracted = extract_pdf(pdf_path)
    save_json(extracted, os.path.join(output_dir, "cleaned_book.json"))

    # Stage 2: Cleaning
    print("[2/5] Cleaning extracted text...")
    cleaned = clean_document(extracted)
    save_json(cleaned, os.path.join(output_dir, "cleaned_book.json"))

    # Stage 3: Structure detection
    print("[3/5] Detecting document structure...")
    structured = detect_document_structure(cleaned)
    save_json(structured, os.path.join(output_dir, "structured_book.json"))

    # Stage 4: Semantic analysis
    print("[4/5] Analysing topics and concepts...")
    semantic = analyse_document(structured)
    save_json(semantic, os.path.join(output_dir, "semantic_book.json"))

    # Stage 5: Importance ranking
    print("[5/5] Ranking important topics...")
    ranked = rank_document(semantic)
    save_json(ranked, os.path.join(output_dir, "ranked_book.json"))

    print("\n===================================")
    print(" ANALYSIS RESULTS")
    print("===================================")

    print("Document:", filename)

    for chapter in ranked.get("chapters", []):
        print("\nCHAPTER:", chapter["title"])

        sections = sorted(
            chapter.get("sections", []),
            key=lambda x: x.get("importance_score", 0),
            reverse=True
        )

        for i, section in enumerate(sections[:10], 1):
            print(
                f"{i}. {section['title']} "
                f"- {section.get('importance_score', 0)}/100"
            )
            print("   Summary:", section.get("summary", ""))
            print("   Concepts:", ", ".join(section.get("concepts", [])))

    print("\nAnalysis completed.")
    print("Results saved inside:", output_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            'Usage: python -m document_ai.analyze_pdf "path\\to\\file.pdf"'
        )
    else:
        analyze_pdf(sys.argv[1])
