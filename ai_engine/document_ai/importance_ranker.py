import json


INPUT_FILE = "document_ai/output/semantic_book.json"
OUTPUT_FILE = "document_ai/output/ranked_book.json"


CORE_TOPICS = {
    "clr",
    "common language runtime",
    "bcl",
    "base class library",
    "cls",
    "common language specification",
    "msil",
    "cil",
    "garbage collector",
    "c# data types",
    "variable declaration",
    "type conversion",
    "operators",
    "decision making",
    "arrays",
    "loops",
    "tuples",
}


def calculate_importance(section):
    title = section.get("title", "").lower()
    word_count = section.get("word_count", 0)
    concepts = section.get("concepts", [])
    relationships = section.get("related_topics", [])

    # 1. Importance from the topic title: maximum 35 points.
    title_score = 10

    if any(topic in title for topic in CORE_TOPICS):
        title_score = 35
    elif any(word in title for word in (
        "introduction",
        "architecture",
        "advantages",
        "characteristics",
        "types",
        "methods",
    )):
        title_score = 25

    # 2. Amount of educational content: maximum 25 points.
    content_score = min(word_count / 100, 1) * 25

    # 3. Number of extracted concepts: maximum 25 points.
    concept_score = min(len(concepts) / 8, 1) * 25

    # 4. Connections to other topics: maximum 15 points.
    relationship_score = min(len(relationships) / 3, 1) * 15

    total = (
        title_score
        + content_score
        + concept_score
        + relationship_score
    )

    return {
        "title_score": round(title_score, 2),
        "content_score": round(content_score, 2),
        "concept_score": round(concept_score, 2),
        "relationship_score": round(relationship_score, 2),
        "importance_score": round(total, 2),
    }


def rank_document(document):
    chapters = []

    for chapter in document.get("chapters", []):
        ranked_sections = []

        for section in chapter.get("sections", []):
            scores = calculate_importance(section)

            ranked_sections.append({
                **section,
                "importance": scores,
            })

        ranked_sections.sort(
            key=lambda item: item["importance"]["importance_score"],
            reverse=True
        )

        for rank, section in enumerate(ranked_sections, start=1):
            section["importance_rank"] = rank

        chapters.append({
            "title": chapter["title"],
            "page_number": chapter["page_number"],
            "sections": ranked_sections,
        })

    return {
        "filename": document.get("filename"),
        "total_pages": document.get("total_pages"),
        "total_chapters": len(chapters),
        "chapters": chapters,
    }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        document = json.load(file)

    print("Ranking topic importance...")

    result = rank_document(document)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("\n========== TOPIC IMPORTANCE RANKING ==========")

    for chapter in result["chapters"]:
        print("\nChapter:", chapter["title"])

        for section in chapter["sections"]:
            score = section["importance"]["importance_score"]

            print(
                f"{section['importance_rank']}. "
                f"{section['title']} — {score}/100"
            )

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()