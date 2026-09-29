comiccraft/static/js/app.js
document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "comic-form"
            );

        const button =
            document.getElementById(
                "submit-button"
            );


        if (!form || !button) {
            return;
        }


        form.addEventListener(
            "submit",
            () => {

                button.disabled = true;


                const span =
                    button.querySelector(
                        "span"
                    );


                if (span) {

                    span.textContent =
                        "Creating comic… This can take a while.";

                }

            }
        );

    }
);