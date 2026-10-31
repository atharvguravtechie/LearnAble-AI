
document.addEventListener("DOMContentLoaded", function () {
    const doubtForm = document.getElementById("doubtForm");
    const questionInput = document.getElementById("question");
    const characterCount = document.getElementById("characterCount");
    const clearButton = document.getElementById("clearButton");
    const askAnotherButton = document.getElementById("askAnotherButton");
    const answerContainer = document.getElementById("doubtAnswer");

    // Character counter
    if (questionInput && characterCount) {
        function updateCharacterCount() {
            characterCount.textContent = questionInput.value.length;
        }

        questionInput.addEventListener("input", updateCharacterCount);
        updateCharacterCount();
    }

    // Clear question
    if (clearButton && questionInput) {
        clearButton.addEventListener("click", function () {
            questionInput.value = "";

            if (characterCount) {
                characterCount.textContent = "0";
            }

            questionInput.focus();
        });
    }

    // Empty question validation
    if (doubtForm && questionInput) {
        doubtForm.addEventListener("submit", function (event) {
            if (!questionInput.value.trim()) {
                event.preventDefault();
                alert("Please enter your question first.");
                questionInput.focus();
            }
        });
    }

    // Ask another question
    if (askAnotherButton) {
        askAnotherButton.addEventListener("click", function () {
            window.location.href = window.location.pathname;
        });
    }

    // Format AI answer
    if (answerContainer) {
        const rawText = answerContainer.textContent || "";
        formatAIAnswer(answerContainer, rawText);
    }

    function formatAIAnswer(container, text) {
        container.replaceChildren();

        const normalizedText = String(text)
            .replace(/\r\n?/g, "\n")

            // Separate named sections, even if Gemini puts everything on one line.
            .replace(
                /\s*(Definition|Explanation|Example|Key Points to Remember|Important Scientific Terms|The Chemical Formula|The Chemical Process)\s*:/gi,
                "\n$1:\n"
            )

            // Separate Markdown headings.
            .replace(/\s*(#{1,6}\s+)/g, "\n$1")

            // Separate bullet points.
            .replace(/\s+([*+-]\s+)/g, "\n$1")

            // Separate numbered points.
            .replace(/\s+(\d+[.)]\s+)/g, "\n$1")

            .trim();

        const lines = normalizedText
            .split("\n")
            .map(line => line.trim())
            .filter(line => line.length > 0);

        let currentList = null;
        let currentListType = null;

        function closeList() {
            currentList = null;
            currentListType = null;
        }

        function addParagraph(content) {
            const paragraph = document.createElement("p");
            paragraph.className = "doubt-answer-paragraph";
            addInlineFormatting(paragraph, content);
            container.appendChild(paragraph);
        }

        function addHeading(content) {
            closeList();

            const heading = document.createElement("h3");
            heading.className = "doubt-answer-heading";
            addInlineFormatting(heading, content);
            container.appendChild(heading);
        }

        function addSectionHeading(content) {
            closeList();

            const heading = document.createElement("h3");
            heading.className = "doubt-answer-section";
            addInlineFormatting(heading, content);
            container.appendChild(heading);
        }

        function addListItem(content, type) {
            if (!currentList || currentListType !== type) {
                closeList();

                currentList = document.createElement(
                    type === "ordered" ? "ol" : "ul"
                );

                currentList.className = "doubt-answer-list";
                currentListType = type;
                container.appendChild(currentList);
            }

            const item = document.createElement("li");
            addInlineFormatting(item, content);
            currentList.appendChild(item);
        }

        lines.forEach(function (line) {
            // Section labels such as Definition:
            const sectionMatch = line.match(
                /^(Definition|Explanation|Example|Key Points to Remember|Important Scientific Terms|The Chemical Formula|The Chemical Process)\s*:\s*(.*)$/i
            );

            if (sectionMatch) {
                addSectionHeading(sectionMatch[1]);

                if (sectionMatch[2].trim()) {
                    addParagraph(sectionMatch[2].trim());
                }

                return;
            }

            // Markdown headings: #, ##, ###
            const headingMatch = line.match(/^#{1,6}\s+(.+)$/);

            if (headingMatch) {
                addHeading(headingMatch[1]);
                return;
            }

            // Unordered lists: *, -, +
            const bulletMatch = line.match(/^[-*+]\s+(.+)$/);

            if (bulletMatch) {
                addListItem(bulletMatch[1], "unordered");
                return;
            }

            // Ordered lists: 1. or 1)
            const numberedMatch = line.match(/^\d+[.)]\s+(.+)$/);

            if (numberedMatch) {
                addListItem(numberedMatch[1], "ordered");
                return;
            }

            // Formula blocks: $$...$$
            if (line.startsWith("$$") && line.endsWith("$$")) {
                closeList();

                const formula = document.createElement("div");
                formula.className = "math-block";
                formula.textContent = line.slice(2, -2).trim();
                container.appendChild(formula);
                return;
            }

            // Normal paragraph
            closeList();
            addParagraph(line);
        });
    }

    // Safe inline Markdown formatting.
    // Uses text nodes, never inserts AI-generated HTML.
    function addInlineFormatting(element, text) {
        const pattern =
            /(\*\*[\s\S]+?\*\*|__[\s\S]+?__|`[^`]+`|\*[^*]+?\*|_[^_]+?_|\\\([\s\S]+?\\\)|\$[^$\n]+\$)/g;

        let lastIndex = 0;
        let match;

        while ((match = pattern.exec(text)) !== null) {
            if (match.index > lastIndex) {
                element.appendChild(
                    document.createTextNode(
                        text.slice(lastIndex, match.index)
                    )
                );
            }

            const token = match[0];
            const node = document.createElement(
                token.startsWith("`") ? "code" : "span"
            );

            if (
                (token.startsWith("**") && token.endsWith("**")) ||
                (token.startsWith("__") && token.endsWith("__"))
            ) {
                const strong = document.createElement("strong");
                strong.textContent = token.slice(2, -2);
                element.appendChild(strong);
            } else if (
                token.startsWith("*") ||
                token.startsWith("_")
            ) {
                const italic = document.createElement("em");
                italic.textContent = token.slice(1, -1);
                element.appendChild(italic);
            } else if (token.startsWith("`")) {
                node.textContent = token.slice(1, -1);
                element.appendChild(node);
            } else {
                node.className = "math-formula";
                node.textContent = token
                    .replace(/^\\\(|\\\)$/g, "")
                    .replace(/^\$|\$$/g, "");
                element.appendChild(node);
            }

            lastIndex = pattern.lastIndex;
        }

        if (lastIndex < text.length) {
            element.appendChild(
                document.createTextNode(text.slice(lastIndex))
            );
        }
    }
});
