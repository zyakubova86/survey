document.addEventListener("DOMContentLoaded", function () {

    function scrollToNext(card) {
        let next = card.nextElementSibling;

        while (next && !next.classList.contains("question-card")) {
            next = next.nextElementSibling;
        }

        if (next) {
            next.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
        setTimeout(() => {
            const input = next.querySelector(
                "input, textarea, select"
            );

            if (input) {
                input.focus();
            }
        }, 200);
    }

    function isAutoNextAllowed(input) {
        const card = input.closest(".question-card");

        if (input.matches("textarea, input[type='number']")) {
            return input.value.trim() !== "";
        }

        if (input.type === "radio") {
            return true;
        }

        // CHECKBOX → NEVER auto-scroll
        if (input.type === "checkbox") {
            return false;
        }

        return false;
    }

    function updateAnsweredState(card) {

        let answered = false;

        // textarea
        const textarea = card.querySelector("textarea");
        if (textarea && textarea.value.trim() !== "") {
            answered = true;
        }

        // number
        const numberInput = card.querySelector("input[type='number']");
        if (numberInput && numberInput.value.trim() !== "") {
            answered = true;
        }

        // radio
        if (card.querySelector("input[type='radio']:checked")) {
            answered = true;
        }

        // checkbox
        if (card.querySelector("input[type='checkbox']:checked")) {
            answered = true;
        }

        if (answered) {
            card.classList.add("answered-question");
        } else {
            card.classList.remove("answered-question");
        }
    }

    document.querySelectorAll(".question-input").forEach(input => {
        input.addEventListener("change", function () {

            const card = this.closest(".question-card");
            // update answered color
            updateAnsweredState(card);

            // auto next
            if (isAutoNextAllowed(this)) {
                setTimeout(() => {
                    scrollToNext(card);
                }, 200);
            }

        });

    });

    document.querySelectorAll("textarea").forEach(textarea => {
        textarea.addEventListener("focus", function () {
            if (this.value.trim() === "") {
                this.value = "";
            }
        });

    });

});