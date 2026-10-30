document.addEventListener("DOMContentLoaded", function () {
    const topicInput = document.getElementById("topic");
    const generateButton = document.querySelector(".generate-notes-button");

    if (generateButton && topicInput) {
        generateButton.addEventListener("click", function (event) {
            if (!topicInput.value.trim()) {
                event.preventDefault();
                alert("Please enter a topic or syllabus first.");
                topicInput.focus();
            }
        });
    }
});