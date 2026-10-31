import json
import re
from collections import Counter


INPUT_FILE = "document_ai/output/structured_book.json"
OUTPUT_FILE = "document_ai/output/semantic_book.json"


STOPWORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and",
    "or", "of", "to", "in", "on", "for", "by", "with",
    "from", "as", "at", "it", "this", "that", "these",
    "those", "be", "been", "being", "can", "could",
    "should", "would", "will", "shall", "may", "might",
    "must", "has", "have", "had", "do", "does", "did",
    "not", "but", "if", "then", "than", "into", "also",
    "which", "who", "what", "when", "where", "how",
    "their", "they", "them", "its", "we", "you", "your",
    "our", "such", "using", "used", "use", "example",
    "examples", "following", "following", "given",
    "shown", "following", "one", "two", "more",
    "each", "other", "same", "different", "following",
    "method", "methods", "following", "etc",
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.]*", text.lower())

    return [
        word for word in words
        if word not in STOPWORDS and len(word) > 2
    ]


def extract_concepts(title, content):
    words = tokenize(content)
    title_words = set(tokenize(title))

    frequencies = Counter(words)

    # Generate candidate single-word and two-word concepts.
    bigrams = []

    for index in range(len(words) - 1):
        first = words[index]
        second = words[index + 1]

        if first not in STOPWORDS and second not in STOPWORDS:
            bigrams.append(first + " " + second)

    bigram_frequencies = Counter(bigrams)

    candidates = []

    for word, count in frequencies.items():
        score = count

        if word in title_words:
            score += 3

        candidates.append((word, score))

    for phrase, count in bigram_frequencies.items():
        score = count * 1.5

        if any(word in title_words for word in phrase.split()):
            score += 3

        candidates.append((phrase, score))

    candidates.sort(key=lambda item: item[1], reverse=True)

    concepts = []

    for concept, score in candidates:
        if concept not in concepts:
            concepts.append(concept)

        if len(concepts) >= 8:
            break

    return concepts


def generate_summary(content):
    content = re.sub(r"\s+", " ", content).strip()

    if not content:
        return "No section text was extracted."

    sentences = re.split(r"(?<=[.!?])\s+", content)

    meaningful = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 5
    ]

    if meaningful:
        summary = " ".join(meaningful[:2])
    else:
        summary = " ".join(content.split()[:40])

    if len(summary.split()) > 65:
        summary = " ".join(summary.split()[:65]) + "..."

    return summary


def calculate_similarity(concepts_a, concepts_b):
    set_a = set(concepts_a)
    set_b = set(concepts_b)

    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))

    return intersection / union


def analyse_section(section):
    title = section.get("title", "")
    content = section.get("content", "")

    concepts = extract_concepts(title, content)
    summary = generate_summary(content)

    return {
        "title": title,
        "page_number": section.get("page_number"),
        "content": content,
        "summary": summary,
        "concepts": concepts,
        "word_count": len(tokenize(content)),
    }


def analyse_document(document):
    analysed_chapters = []

    for chapter in document.get("chapters", []):
        analysed_sections = []

        for section in chapter.get("sections", []):
            analysed_sections.append(analyse_section(section))

        # Find relationships between sections.
        for section in analysed_sections:
            relationships = []

            for other in analysed_sections:
                if section["title"] == other["title"]:
                    continue

                similarity = calculate_similarity(
                    section["concepts"],
                    other["concepts"]
                )

                if similarity >= 0.10:
                    relationships.append({
                        "related_topic": other["title"],
                        "similarity": round(similarity, 3),
                    })

            relationships.sort(
                key=lambda item: item["similarity"],
                reverse=True
            )

            section["related_topics"] = relationships[:3]

        analysed_chapters.append({
            "title": chapter["title"],
            "page_number": chapter["page_number"],
            "sections": analysed_sections,
        })

    return {
        "filename": document.get("filename"),
        "total_pages": document.get("total_pages"),
        "total_chapters": len(analysed_chapters),
        "chapters": analysed_chapters,
    }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        document = json.load(file)

    print("Running semantic analysis...")

    result = analyse_document(document)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("\n========== SEMANTIC ANALYSIS ==========")
    print("Document:", result["filename"])

    for chapter in result["chapters"]:
        print("\nChapter:", chapter["title"])

        for section in chapter["sections"]:
            print("\nTopic:", section["title"])
            print("Words:", section["word_count"])
            print("Concepts:", ", ".join(section["concepts"]))
            print("Summary:", section["summary"])
            print("Related:", [
                item["related_topic"]
                for item in section["related_topics"]
            ])

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()