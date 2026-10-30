document.addEventListener("DOMContentLoaded", function () {
    const questionInput = document.getElementById("question");
    const characterCount = document.getElementById("characterCount");
    const clearButton = document.getElementById("clearButton");
    const doubtForm = document.getElementById("doubtForm");
    const askAnotherButton = document.getElementById("askAnotherButton");

    function updateCharacterCount() {
        if (!questionInput || !characterCount) return;

        const count = questionInput.value.length;
        characterCount.textContent = count + " characters";
    }

    if (questionInput) {
        updateCharacterCount();
        questionInput.addEventListener("input", updateCharacterCount);
    }

    if (clearButton) {
        clearButton.addEventListener("click", function () {
            questionInput.value = "";
            updateCharacterCount();
            questionInput.focus();
        });
    }

    if (doubtForm) {
        doubtForm.addEventListener("submit", function (event) {
            if (!questionInput.value.trim()) {
                event.preventDefault();
                questionInput.focus();
                alert("Please enter your question first.");
            }
        });
    }

    if (askAnotherButton) {
        askAnotherButton.addEventListener("click", function () {
            window.location.href = window.location.pathname;
        });
    }
});