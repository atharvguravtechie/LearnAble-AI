import re


WATERMARK_PATTERNS = [
    r"^SANGOLA COLLEGE SANGOLA",
    r"^SHIVRATNA HONRAO$",
    r"^SHVRATNA HONRAO$",
    r"^B\.Sc\.",
    r"^\d+\s*\|?\s*Page$",
    r"^\d+\|Page$",
]

UNIT_PATTERN = re.compile(
    r"^(UNIT|CHAPTER|MODULE)\s*[-:]?\s*[IVX0-9]+\b",
    re.IGNORECASE
)

NUMBERED_TOPIC_PATTERN = re.compile(
    r"^\d+\)\s*(CLR|BCL|CLS|MSIL|CIL|Garbage Collector)\b",
    re.IGNORECASE
)

NUMBERED_CONTROL_PATTERN = re.compile(
    r"^\d+\)\s*(if\b|if-else|nested if|switch|for\b|while\b)",
    re.IGNORECASE
)

STARRED_HEADING_PATTERN = re.compile(r"^\s*\*\s*(.+)$")

KNOWN_HEADING_STARTS = (
    "components of ",
    "advantages of ",
    "characteristics of ",
    "variable naming conventions",
    "variable declaration",
    "initializing variables",
    "accepting values from user",
    "c# data types",
    "c# input",
    "c# operators",
    "c# operator precedence",
    "c# decision making",
    "type conversion",
    "nullable types",
    "null coalescing operator",
    "elvis operator",
    "type inference",
    "console input output",
    "complex data types",
    "examples on ",
    "if-else statement",
    "nested if",
    "switch case",
)

CODE_STARTS = (
    "using ",
    "public ",
    "private ",
    "static ",
    "class ",
    "namespace ",
    "console.",
    "int ",
    "char ",
    "float ",
    "double ",
    "string ",
    "var ",
    "if ",
    "else",
    "for ",
    "while ",
    "return ",
)


def normalize_line(line):
    line = line.strip()
    line = re.sub(r"^[•▪»=\-]+\s*", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def is_watermark(line):
    return any(
        re.search(pattern, line, re.IGNORECASE)
        for pattern in WATERMARK_PATTERNS
    )


def clean_heading_text(line):
    line = normalize_line(line)
    line = re.sub(r"^\*+\s*", "", line)
    return line.strip(" -*:")


def is_heading(line):
    original = line.strip()

    if not original or len(original) > 120:
        return False

    if is_watermark(original):
        return False

    if UNIT_PATTERN.match(original):
        return False

    normalized = normalize_line(original)
    lower = normalized.lower()

    # Reject obvious code and output.
    if lower.startswith(CODE_STARTS):
        return False

    if "console.writeline" in lower:
        return False

    if "nested tuple element=" in lower:
        return False

    # Numbered technical headings.
    if NUMBERED_TOPIC_PATTERN.match(original):
        return True

    if NUMBERED_CONTROL_PATTERN.match(original):
        return True

    # Starred headings: accept short labels, not long explanations.
    starred = STARRED_HEADING_PATTERN.match(original)

    if starred:
        content = starred.group(1).strip()

        # Some OCR lines combine a heading and its explanation.
        if "-" in content:
            prefix = content.split("-", 1)[0].strip()
            if 3 <= len(prefix) <= 45:
                return True

        if len(content) <= 55:
            return True

        return False

    # Known heading phrases.
    if lower in KNOWN_HEADING_STARTS:
        return True

    if any(
        lower.startswith(prefix)
        and len(normalized) <= 65
        for prefix in KNOWN_HEADING_STARTS
    ):
        return True

    exact_headings = {
        "introduction",
        "definition",
        "net core",
        "c# basics",
        "nested loops",
        "methods",
        "nested tuple",
        "garbage collector",
        "clr (common language runtime)",
        "bcl (base class library)",
        "cls (common language specification)",
    }

    if lower.rstrip(" -:.") in exact_headings:
        return True

    return False
    original = line.strip()

    if not original or len(original) > 120:
        return False

    if is_watermark(original):
        return False

    if UNIT_PATTERN.match(original):
        return False

    # Starred headings used throughout the textbook.
    starred_match = STARRED_HEADING_PATTERN.match(original)

    if starred_match:
        starred_text = starred_match.group(1).strip()
        lower_text = starred_text.lower()

        if lower_text.startswith((
            "clr provides",
            "it is ",
            "the ",
        )):
            return False

        return True

    # Numbered technical topic headings.
    if NUMBERED_TOPIC_PATTERN.match(original):
        return True

    # Numbered programming constructs.
    if NUMBERED_CONTROL_PATTERN.match(original):
        return True

    normalized = normalize_line(original)
    lower = normalized.lower()

    # Reject obvious code lines.
    if lower.startswith(CODE_STARTS):
        return False

    if lower.startswith(KNOWN_HEADING_STARTS):
        return True

    exact_headings = {
        "methods",
        "nested loops",
        "nested tuple",
        "net core",
        "garbage collector",
        "fcl (framework class library)",
        "cts (common type system)",
    }

    if lower.rstrip(".") in exact_headings:
        return True

    return False


def extract_heading(line):
    heading = clean_heading_text(line)

    heading = re.sub(r"^\d+\)\s*", "", heading)

    # Extract the heading before an explanation joined by a hyphen.
    if "-" in heading:
        prefix = heading.split("-", 1)[0].strip()

        if 3 <= len(prefix) <= 45:
            heading = prefix

    split_markers = [
        "The first three components",
        "A tuple in C#",
        "Operators in C# are",
        "Data type specify",
        "Variable name may consist",
    ]

    for marker in split_markers:
        position = heading.lower().find(marker.lower())

        if position > 0:
            heading = heading[:position].strip()
            break

    return heading.strip(" -*:")

def detect_structure(document_data):
    pages = document_data.get("pages", [])

    chapters = []
    current_chapter = None
    current_section = None

    for page in pages:
        page_number = page.get("page_number")
        page_text = page.get("cleaned_text", "")

        for raw_line in page_text.splitlines():
            line = raw_line.strip()

            if not line or is_watermark(line):
                continue

            # Detect a new chapter.
            if UNIT_PATTERN.match(line):
                current_chapter = {
                    "title": clean_heading_text(line),
                    "page_number": page_number,
                    "sections": [],
                }

                chapters.append(current_chapter)
                current_section = None
                continue

            if current_chapter is None:
                continue

            # Detect a new section.
            if is_heading(line):
                title = extract_heading(line)

                if len(title) < 3:
                    continue

                sections = current_chapter["sections"]

                # Avoid consecutive duplicate headings.
                if sections and sections[-1]["title"].lower() == title.lower():
                    current_section = sections[-1]
                    continue

                current_section = {
                    "title": title,
                    "page_number": page_number,
                    "content": [],
                }

                sections.append(current_section)

            elif current_section is not None:
                # Attach ordinary text to the current section.
                if not is_watermark(line):
                    current_section["content"].append(line)

    # Convert content lists into strings.
    for chapter in chapters:
        for section in chapter["sections"]:
            section["content"] = "\n".join(section["content"]).strip()

    return {
        "filename": document_data.get("filename", "Unknown document"),
        "total_pages": document_data.get("total_pages", len(pages)),
        "total_chapters": len(chapters),
        "chapters": chapters,
    }

def detect_document_structure(document_data):
    return detect_structure(document_data)