
document.addEventListener("DOMContentLoaded", function () {

    // HTML elements
    const form = document.getElementById("teacherForm");
    const questionInput = document.getElementById("questionInput");
    const chatMessages = document.getElementById("chatMessages");
    const languageSelect = document.getElementById("languageSelect");
    const clearChatButton = document.getElementById("clearChat");
    const voiceButton = document.getElementById("voiceInput");
    const sendButton = document.getElementById("sendQuestion");

    // Backend API URL
    const API_URL = "http://127.0.0.1:8001/api/teacher/ask/";
    // Get Django CSRF token
function getCSRFToken() {
    const cookie = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="));

    if (cookie) {
        return decodeURIComponent(cookie.split("=")[1]);
    }

    const hiddenToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
    );

    return hiddenToken ? hiddenToken.value : "";
}

    // Browser voice recognition
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    let recognition = null;

    const backendLanguages = {
        "en-US": "English",
        "hi-IN": "Hindi",
        "mr-IN": "Marathi"
    };

    const languageContent = {
        "en-US": {
            welcome: "Hello! I'm Alex, your learning companion. What would you like to learn today? You can ask me a question or choose one of the suggestions below.",
            placeholder: "Ask your teacher anything...",
            tryAsking: "TRY ASKING",
            teacherName: "Alex · AI Teacher",
            listen: "Listen",
            you: "You"
        },

        "hi-IN": {
            welcome: "नमस्ते! मैं एलेक्स हूँ, आपका सीखने का साथी। आज आप क्या सीखना चाहते हैं? आप मुझसे कोई भी प्रश्न पूछ सकते हैं।",
            placeholder: "अपने शिक्षक से कुछ भी पूछें...",
            tryAsking: "यह पूछकर देखें",
            teacherName: "एलेक्स · AI शिक्षक",
            listen: "सुनें",
            you: "आप"
        },

        "mr-IN": {
            welcome: "नमस्कार! मी अॅलेक्स आहे, तुमचा शिकण्याचा साथीदार. आज तुम्हाला काय शिकायचे आहे? तुम्ही मला कोणताही प्रश्न विचारू शकता.",
            placeholder: "तुमच्या शिक्षकाला काहीही विचारा...",
            tryAsking: "हे प्रश्न विचारून पाहा",
            teacherName: "अॅलेक्स · AI शिक्षक",
            listen: "ऐका",
            you: "तुम्ही"
        }
    };

    function getLanguage() {
        return languageSelect.value || "en-US";
    }

    function getContent() {
        return languageContent[getLanguage()] || languageContent["en-US"];
    }

    function getBackendLanguage() {
        return backendLanguages[getLanguage()] || "English";
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Safely format inline Markdown
    function renderInlineMarkdown(text, parent) {

        const pattern =
            /(\*\*.*?\*\*|__.*?__|`.*?`|\$[^$\n]+\$|\*[^*\n]+\*)/g;

        let lastIndex = 0;
        let match;

        while ((match = pattern.exec(text)) !== null) {

            if (match.index > lastIndex) {
                parent.appendChild(
                    document.createTextNode(
                        text.slice(lastIndex, match.index)
                    )
                );
            }

            const token = match[0];
            let element;

            if (
                token.startsWith("**") ||
                token.startsWith("__")
            ) {
                element = document.createElement("strong");
                element.textContent = token.slice(2, -2);

            } else if (token.startsWith("`")) {
                element = document.createElement("code");
                element.textContent = token.slice(1, -1);

            } else if (token.startsWith("$")) {
                element = document.createElement("span");
                element.className = "math-formula";
                element.textContent = token.slice(1, -1);

            } else {
                element = document.createElement("em");
                element.textContent = token.slice(1, -1);
            }

            parent.appendChild(element);
            lastIndex = pattern.lastIndex;
        }

        if (lastIndex < text.length) {
            parent.appendChild(
                document.createTextNode(text.slice(lastIndex))
            );
        }
    }

    // Convert Gemini Markdown into properly formatted HTML elements
    // Uses DOM creation and textContent, not unsafe HTML insertion.
    function renderMarkdown(text, container) {

        container.innerHTML = "";

        const normalizedText = String(text)
    .replace(/\r\n?/g, "\n")
    // Put Markdown headings on separate lines
    .replace(/\s+(?=#{1,6}\s)/g, "\n")
    // Separate named sections
    .replace(
        /\s+(?=(?:Definition|Explanation|Example|Key Points to Remember|Important Scientific Terms|The Chemical Formula|The Chemical Process)\s*:)/gi,
        "\n"
    )
    // Separate bullet points and numbered steps
    .replace(/\s+(?=[-*+]\s+)/g, "\n")
    .replace(/\s+(?=\d+[.)]\s+)/g, "\n");

const lines = normalizedText.split("\n");

        let currentList = null;
        let currentListType = null;

        function closeList() {
            currentList = null;
            currentListType = null;
        }

        function addFormattedBlock(tag, content, className) {

            const element = document.createElement(tag);

            if (className) {
                element.className = className;
            }

            renderInlineMarkdown(content, element);
            container.appendChild(element);
        }

        for (let i = 0; i < lines.length; i++) {

            const line = lines[i].trim();

            if (!line) {
                closeList();
                continue;
            }

            // Display block mathematical formulas
            if (line.startsWith("$$")) {

                closeList();

                let formula = line.replace(/\$\$/g, "");

                while (
                    !line.endsWith("$$") &&
                    i + 1 < lines.length
                ) {
                    i++;
                    const nextLine = lines[i];

                    if (nextLine.includes("$$")) {
                        formula += "\n" +
                            nextLine.replace(/\$\$/g, "");
                        break;
                    }

                    formula += "\n" + nextLine;
                }

                const formulaBox = document.createElement("div");
                formulaBox.className = "math-block";
                formulaBox.textContent = formula.trim();

                container.appendChild(formulaBox);
                continue;
            }

            // Headings
            const headingMatch = line.match(/^(#{1,4})\s+(.+)$/);

            if (headingMatch) {
                closeList();

                const level = headingMatch[1].length;
                addFormattedBlock(
                    "h" + (level + 1),
                    headingMatch[2],
                    "ai-answer-heading"
                );
                continue;
            }

            // Bold section labels such as Definition:
            const sectionMatch = line.match(
                /^(Definition|Explanation|Example|Key Points to Remember|Conclusion|Summary|Important Scientific Terms|The Chemical Formula|The Chemical Process)\s*:\s*(.*)$/i
            );

            if (sectionMatch) {

                closeList();

                addFormattedBlock(
                    "h3",
                    sectionMatch[1],
                    "ai-answer-heading"
                );

                if (sectionMatch[2].trim()) {
                    addFormattedBlock(
                        "p",
                        sectionMatch[2],
                        "ai-answer-paragraph"
                    );
                }

                continue;
            }

            // Unordered lists
            const unorderedMatch = line.match(/^[-*+]\s+(.+)$/);

            if (unorderedMatch) {

                if (currentListType !== "ul") {
                    closeList();
                    currentList = document.createElement("ul");
                    currentList.className = "ai-answer-list";
                    currentListType = "ul";
                    container.appendChild(currentList);
                }

                const item = document.createElement("li");
                renderInlineMarkdown(unorderedMatch[1], item);
                currentList.appendChild(item);
                continue;
            }

            // Numbered lists
            const orderedMatch = line.match(/^\d+[.)]\s+(.+)$/);

            if (orderedMatch) {

                if (currentListType !== "ol") {
                    closeList();
                    currentList = document.createElement("ol");
                    currentList.className = "ai-answer-list";
                    currentListType = "ol";
                    container.appendChild(currentList);
                }

                const item = document.createElement("li");
                renderInlineMarkdown(orderedMatch[1], item);
                currentList.appendChild(item);
                continue;
            }

            // Blockquotes
            if (line.startsWith(">")) {

                closeList();

                addFormattedBlock(
                    "blockquote",
                    line.replace(/^>\s?/, ""),
                    "ai-answer-quote"
                );
                continue;
            }

            // Normal paragraphs
            closeList();

            addFormattedBlock(
                "p",
                line,
                "ai-answer-paragraph"
            );
        }
    }

    // Add a message to the conversation
    function addMessage(text, sender) {

        const contentText = getContent();

        const message = document.createElement("div");

        message.className = sender === "student"
            ? "chat-message student-message"
            : "chat-message teacher-message";

        const avatar = document.createElement("div");
        avatar.className = "message-avatar";

        avatar.innerHTML = sender === "student"
            ? '<i class="bi bi-person-fill"></i>'
            : '<i class="bi bi-mortarboard-fill"></i>';

        const content = document.createElement("div");
        content.className = "message-content";

        const name = document.createElement("div");
        name.className = "message-name";

        name.textContent = sender === "student"
            ? contentText.you
            : contentText.teacherName;

        const bubble = document.createElement("div");
        bubble.className = "message-bubble";

        if (sender === "teacher") {
            renderMarkdown(text, bubble);
        } else {
            bubble.textContent = text;
        }

        content.appendChild(name);
        content.appendChild(bubble);

        if (sender === "teacher") {

            const actions = document.createElement("div");
            actions.className = "message-actions";

            const speakButton = document.createElement("button");
            speakButton.type = "button";
            speakButton.className = "speak-button";

            speakButton.innerHTML =
                `<i class="bi bi-volume-up"></i> ${contentText.listen}`;

            speakButton.addEventListener("click", function () {
                speakText(text);
            });

            actions.appendChild(speakButton);
            content.appendChild(actions);
        }

        message.appendChild(avatar);
        message.appendChild(content);

        chatMessages.appendChild(message);
        scrollToBottom();
    }

    // Text-to-speech
    function speakText(text) {

        if (!("speechSynthesis" in window)) {
            alert("Speech playback is not supported in this browser.");
            return;
        }

        window.speechSynthesis.cancel();

        const selectedLanguage = getLanguage();

        // Remove Markdown symbols before speaking
        const cleanText = text
            .replace(/#{1,6}\s/g, "")
            .replace(/\*\*(.*?)\*\*/g, "$1")
            .replace(/\*(.*?)\*/g, "$1")
            .replace(/`(.*?)`/g, "$1")
            .replace(/\$/g, "")
            .replace(/^[-*+]\s/gm, "")
            .replace(/^\d+[.)]\s/gm, "");

        const utterance = new SpeechSynthesisUtterance(cleanText);

        utterance.lang = selectedLanguage;
        utterance.rate = 0.85;
        utterance.pitch = 1;

        function findVoice() {

            const voices = window.speechSynthesis.getVoices();

            let matchingVoice = voices.find(function (voice) {
                return voice.lang.toLowerCase() ===
                    selectedLanguage.toLowerCase();
            });

            if (!matchingVoice) {
                const languageCode =
                    selectedLanguage.split("-")[0].toLowerCase();

                matchingVoice = voices.find(function (voice) {
                    return voice.lang.toLowerCase().startsWith(languageCode);
                });
            }

            if (!matchingVoice) {

                if (selectedLanguage === "mr-IN") {
                    alert(
                        "Marathi speech voice is not available on your computer. " +
                        "Please install a Marathi text-to-speech voice or use a browser that supports one."
                    );
                    return;
                }

                alert("A voice for the selected language is not available.");
                return;
            }

            utterance.voice = matchingVoice;
            window.speechSynthesis.speak(utterance);
        }

        const voices = window.speechSynthesis.getVoices();

        if (voices.length > 0) {
            findVoice();
        } else {
            window.speechSynthesis.addEventListener(
                "voiceschanged",
                findVoice,
                { once: true }
            );
        }
    }

    // Update welcome message when language changes
    function updateWelcomeMessage() {

        const content = getContent();

        chatMessages.innerHTML = "";

        const message = document.createElement("div");
        message.className = "chat-message teacher-message";

        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.innerHTML = '<i class="bi bi-mortarboard-fill"></i>';

        const messageContent = document.createElement("div");
        messageContent.className = "message-content";

        const name = document.createElement("div");
        name.className = "message-name";
        name.textContent = content.teacherName;

        const bubble = document.createElement("div");
        bubble.className = "message-bubble";
        bubble.textContent = content.welcome;

        const actions = document.createElement("div");
        actions.className = "message-actions";

        const listenButton = document.createElement("button");
        listenButton.type = "button";
        listenButton.className = "speak-button";

        listenButton.innerHTML =
            `<i class="bi bi-volume-up"></i> ${content.listen}`;

        listenButton.addEventListener("click", function () {
            speakText(content.welcome);
        });

        actions.appendChild(listenButton);

        messageContent.appendChild(name);
        messageContent.appendChild(bubble);
        messageContent.appendChild(actions);

        message.appendChild(avatar);
        message.appendChild(messageContent);

        chatMessages.appendChild(message);

        questionInput.placeholder = content.placeholder;

        const suggestionHeading =
            document.querySelector(".suggestion-area > p");

        if (suggestionHeading) {
            suggestionHeading.textContent = content.tryAsking;
        }

        scrollToBottom();
    }

    // Send question to Gemini backend
    async function sendQuestion(question) {

        const cleanQuestion = question.trim();

        if (!cleanQuestion || sendButton.disabled) {
            return;
        }

        addMessage(cleanQuestion, "student");

        questionInput.value = "";
        sendButton.disabled = true;

        const originalButtonHTML = sendButton.innerHTML;

        sendButton.innerHTML =
            '<i class="bi bi-hourglass-split"></i> Thinking...';

        try {

            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: cleanQuestion,
                    language: getBackendLanguage()
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || data.detail ||
                    "Unable to get an answer from the AI Teacher."
                );
            }

            if (!data.success || !data.answer) {
                throw new Error(
                    data.error || "The AI did not return an answer."
                );
            }

            addMessage(data.answer, "teacher");
            // Save the successfully answered question to Progress Tracker
try {
    const csrfToken = getCSRFToken();

    const progressResponse = await fetch(
        "/teacher/record-activity/",
        {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                question: cleanQuestion
            })
        }
    );

    if (!progressResponse.ok) {
        console.error(
            "Could not save AI Teacher activity:",
            await progressResponse.text()
        );
    }
} catch (progressError) {
    console.error("Progress recording error:", progressError);
}

        } catch (error) {

            console.error("AI Teacher API error:", error);

            addMessage(
                "Sorry, I could not connect to the AI Teacher. " +
                error.message +
                " Please check that your backend server is running on port 8001 and try again.",
                "teacher"
            );

        } finally {

            sendButton.disabled = false;
            sendButton.innerHTML = originalButtonHTML;
            questionInput.focus();
        }
    }

    // Send typed questions
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        sendQuestion(questionInput.value);
    });

    // Suggested questions
    document.querySelectorAll(".suggestion-button").forEach(function (button) {

        button.addEventListener("click", function () {
            sendQuestion(button.getAttribute("data-question") || "");
        });

    });

    // Change language
    languageSelect.addEventListener("change", function () {

        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }

        if (recognition) {
            recognition.stop();
        }

        updateWelcomeMessage();
    });

    // Clear chat
    clearChatButton.addEventListener("click", function () {

        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }

        updateWelcomeMessage();
    });

    // Voice input
    if (SpeechRecognition) {

        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        voiceButton.addEventListener("click", function () {

            recognition.lang = getLanguage();

            try {
                recognition.start();
            } catch (error) {
                console.log("Voice recognition could not start:", error);
            }

        });

        recognition.onstart = function () {
            voiceButton.classList.add("recording");
        };

        recognition.onresult = function (event) {

            const transcript = event.results[0][0].transcript;

            questionInput.value = transcript;
            questionInput.focus();
        };

        recognition.onerror = function (event) {

            console.log("Voice recognition error:", event.error);

            alert(
                "Voice input could not start. Check microphone permission and try again."
            );
        };

        recognition.onend = function () {
            voiceButton.classList.remove("recording");
        };

    } else {

        voiceButton.addEventListener("click", function () {
            alert(
                "Voice input is not supported in this browser. Please use Google Chrome or type your question."
            );
        });

    }

    // Load welcome message
    updateWelcomeMessage();

});
