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

        // Lokaler Log im Browser zur Kontrolle
        console.log("LOG: Klick erkannt! Sende Nachricht zur Prüfung an das Backend...");

        // Sende die Daten an background.js, welches sie an den Python Server weiterreicht
        chrome.runtime.sendMessage({ type: "VERIFY_CONTENT", text: messageText }, (response) => {
            console.log("LOG: Server-Antwort erhalten. Check dein VS-Code Terminal!");
        });
    }, true);
}

initGuard();