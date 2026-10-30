document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("teacherForm");
    const questionInput = document.getElementById("questionInput");
    const chatMessages = document.getElementById("chatMessages");
    const languageSelect = document.getElementById("languageSelect");
    const clearChatButton = document.getElementById("clearChat");
    const voiceButton = document.getElementById("voiceInput");
    const sendButton = document.getElementById("sendQuestion");

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    let recognition = null;

    const languageContent = {
        "en-US": {
            welcome: "Hello! I'm Alex, your learning companion. What would you like to learn today? You can ask me a question or choose one of the suggestions below.",
            demo: "Thanks for your question! I am currently running in frontend demo mode. Gemini AI will be connected in a later step so I can provide a detailed, personalized explanation.",
            placeholder: "Ask your teacher anything...",
            tryAsking: "TRY ASKING",
            teacherName: "Alex · AI Teacher",
            listen: "Listen",
            you: "You"
        },

        "hi-IN": {
            welcome: "नमस्ते! मैं एलेक्स हूँ, आपका सीखने का साथी। आज आप क्या सीखना चाहते हैं? आप मुझसे कोई भी प्रश्न पूछ सकते हैं।",
            demo: "आपके प्रश्न के लिए धन्यवाद! अभी मैं फ्रंटएंड डेमो मोड में काम कर रहा हूँ। आगे के चरण में Gemini AI जोड़ा जाएगा, जिससे मैं आपको विस्तार से और आपकी आवश्यकता के अनुसार समझा सकूँगा।",
            placeholder: "अपने शिक्षक से कुछ भी पूछें...",
            tryAsking: "यह पूछकर देखें",
            teacherName: "एलेक्स · AI शिक्षक",
            listen: "सुनें",
            you: "आप"
        },

        "mr-IN": {
            welcome: "नमस्कार! मी अॅलेक्स आहे, तुमचा शिकण्याचा साथीदार. आज तुम्हाला काय शिकायचे आहे? तुम्ही मला कोणताही प्रश्न विचारू शकता.",
            demo: "तुमच्या प्रश्नाबद्दल धन्यवाद! सध्या मी फ्रंटएंड डेमो मोडमध्ये काम करत आहे. पुढील टप्प्यात Gemini AI जोडले जाईल, ज्यामुळे मी तुम्हाला सविस्तर आणि तुमच्या गरजेनुसार समजावून सांगू शकेन.",
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

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

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
        bubble.textContent = text;

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

    function speakText(text) {

    if (!("speechSynthesis" in window)) {
        alert("Speech playback is not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel();

    const selectedLanguage = getLanguage();
    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = selectedLanguage;
    utterance.rate = 0.85;
    utterance.pitch = 1;

    function findVoice() {

        const voices = window.speechSynthesis.getVoices();

        // Find an exact language match first.
        let matchingVoice = voices.find(function (voice) {
            return voice.lang.toLowerCase() ===
                selectedLanguage.toLowerCase();
        });

        // Try a regional match, such as mr instead of mr-IN.
        if (!matchingVoice) {
            const languageCode = selectedLanguage.split("-")[0].toLowerCase();

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

    function sendQuestion(question) {

        const cleanQuestion = question.trim();

        if (!cleanQuestion || sendButton.disabled) {
            return;
        }

        addMessage(cleanQuestion, "student");

        questionInput.value = "";
        sendButton.disabled = true;

        window.setTimeout(function () {

            const response = getContent().demo;

            addMessage(response, "teacher");

            sendButton.disabled = false;
            questionInput.focus();

        }, 500);
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

    // Voice recognition
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

    // Load the correct welcome message on page opening
    updateWelcomeMessage();

});