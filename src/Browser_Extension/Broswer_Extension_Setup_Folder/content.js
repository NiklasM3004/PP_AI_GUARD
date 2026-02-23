function initGuard() {
    console.log("Gemini Guard aktiv: Überwachung des Senden-Buttons gestartet.");

    document.addEventListener('click', async (event) => {
        // Wir suchen den Button mit der KLASSE send-button (daher der Punkt)
        const btn = event.target.closest('button.send-button');
        
        if (!btn) return;
        
        if (btn.dataset.checked === "true") {
            btn.dataset.checked = "false"; // Zurücksetzen für den nächsten Klick
            return; 
        }

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
                // FALL 1: Sensitive Daten gefunden -> Blockieren
                console.error("GUARD: Blockiert! Sensitive Daten gefunden.");
                alert("🛑 GEMINI GUARD WARNUNG:\n\nIn deiner Nachricht wurden sensible Daten gefunden.");
            } 
            else if (response && response.is_sensitive === false) {
                // FALL 2: Server sagt OK -> Jetzt wirklich senden
                console.log("GUARD: Alles okay. Nachricht ist sicher. Sende jetzt...");
                
                btn.dataset.checked = "true"; // Marker setzen
                btn.click(); // Erneuten Klick auslösen
            } 
            else {
                // FALL 3: Technischer Fehler (Server/Background-Script antwortet nicht)
                console.error("GUARD: Fehler bei der Prüfung. Aus Sicherheitsgründen blockiert.");
                alert("⚠️ Fehler: Die Sicherheitsprüfung konnte nicht durchgeführt werden. Bitte lade die Seite neu.");
            }
        });
    }, true);
}

initGuard();