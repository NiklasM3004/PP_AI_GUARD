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
            if (response && response.is_sensitive) {
                // ALARM: Wenn der Server "true" zurückgibt
                console.error("GUARD: Blockiert! Sensitive Daten gefunden.");
                alert("🛑 GEMINI GUARD WARNUNG:\n\nIn deiner Nachricht wurden sensible Daten (z. B. Email, Passwort oder API-Key) gefunden.\n\nDer Sendevorgang wurde gestoppt.");
            } else if (response) {
                console.log("GUARD: Alles okay. Nachricht ist sicher.");
                // Hier könnte man später btn.click() einbauen, um automatisch zu senden
            } else {
                console.error("GUARD: Keine Antwort vom Background-Script.");
            }
        });
    }, true);
}

initGuard();