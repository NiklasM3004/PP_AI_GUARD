function initGuard() {
    console.log("Gemini Guard aktiv: Überwachung des Senden-Buttons gestartet.");

    document.addEventListener('click', async (event) => {
        // Wir suchen den Button mit der KLASSE send-button (daher der Punkt)
        const btn = event.target.closest('button.send-button');
        
        if (!btn) return;

        // Wir verhindern das Senden, damit wir erst prüfen können
        event.preventDefault();
        event.stopImmediatePropagation();

        // Text aus dem Feld auslesen
        const inputField = document.querySelector('.ql-editor.textarea');
        const messageText = inputField ? inputField.innerText : "";

       if (messageText === "") {
            console.warn("GUARD: Sendeversuch mit leerem Text erkannt.");
        } else {
            console.log("GUARD: Sende Inhalt zur Prüfung:", messageText);
        }

        chrome.runtime.sendMessage({ type: "VERIFY_CONTENT", text: messageText }, (response) => {
            // LOG für die Antwort
            if (response) {
                console.log("GUARD: Antwort vom Server erhalten:", response);
            } else {
                console.error("GUARD: Keine Antwort vom Background-Script erhalten!");
            }
        });
    }, true);
}

initGuard();