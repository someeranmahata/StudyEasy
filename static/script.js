

    const textarea =
        document.getElementById("message");

    const sendButton =
        document.getElementById("send-button");

    const form =
        document.getElementById("chat-form");

    const pdfInput =
        document.getElementById("pdf");

    const fileName =
        document.getElementById("file-name");

    const messages =
        document.getElementById("messages");


    /* =====================================
       ENABLE / DISABLE SEND BUTTON
    ===================================== */

    function updateSendButton() {

        const hasText =
            textarea.value.trim().length > 0;

        const hasFile =
            pdfInput.files.length > 0;

        sendButton.disabled =
            !(hasText || hasFile);
    }


    textarea.addEventListener(
        "input",
        updateSendButton
    );


    pdfInput.addEventListener(
        "change",
        function () {

            if (pdfInput.files.length > 0) {

                fileName.textContent =
                    pdfInput.files[0].name;

            } else {

                fileName.textContent = "";

            }

            updateSendButton();
        }
    );


    /* =====================================
       ENTER TO SEND
    ===================================== */

    textarea.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                if (!sendButton.disabled) {
                    form.submit();
                }

            }

        }
    );


    /* =====================================
       AUTO RESIZE TEXTAREA
    ===================================== */

    textarea.addEventListener(
        "input",
        function () {

            this.style.height = "auto";

            this.style.height =
                Math.min(
                    this.scrollHeight,
                    150
                ) + "px";

        }
    );


    /* =====================================
       SCROLL TO BOTTOM
    ===================================== */

    function scrollToBottom() {

        messages.scrollTop =
            messages.scrollHeight;

    }


    window.addEventListener(
        "load",
        scrollToBottom
    );
