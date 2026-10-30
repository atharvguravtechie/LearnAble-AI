
document.addEventListener("DOMContentLoaded", function () {
    const quizForm = document.getElementById("quizForm");
    const answeredCount = document.getElementById("answeredCount");

    if (!quizForm) return;

    function updateAnsweredCount() {
        const questionGroups = new Set();

        quizForm.querySelectorAll('input[type="radio"]:checked').forEach(input => {
            questionGroups.add(input.name);
        });

        if (answeredCount) {
            answeredCount.textContent = questionGroups.size;
        }
    }

    quizForm.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener("change", updateAnsweredCount);
    });

    quizForm.addEventListener("submit", function (event) {
        const totalQuestions = new Set(
            Array.from(
                quizForm.querySelectorAll('input[type="radio"]')
            ).map(input => input.name)
        ).size;

        const answeredQuestions = new Set(
            Array.from(
                quizForm.querySelectorAll('input[type="radio"]:checked')
            ).map(input => input.name)
        ).size;

        if (answeredQuestions < totalQuestions) {
            const confirmSubmit = confirm(
                `You have answered ${answeredQuestions} out of ${totalQuestions} questions. Do you still want to submit?`
            );

            if (!confirmSubmit) {
                event.preventDefault();
            }
        }
    });

    updateAnsweredCount();
});
