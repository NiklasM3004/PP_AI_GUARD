 function initGuard() {
    console.log("Gemini Guard aktiv: Überwachung des Senden-Buttons gestartet.");

    document.addEventListener('click', async (event) => {
        // 1. Prüfen, ob der Senden-Button geklickt wurde
        const btn = event.target.closest('button.send-button');
        if (!btn) return;

        // Falls wir den Button gerade selbst "geklickt" haben nach erfolgreicher Prüfung
        if (btn.dataset.checked === "true") {
            btn.dataset.checked = "false"; 
            return; 
        }

        // 2. Standard-Senden stoppen für die Sicherheitsprüfung
        event.preventDefault();
        event.stopImmediatePropagation();

        // 3. Nachrichtentext auslesen
        const inputField = document.querySelector('.ql-editor.textarea');
        const messageText = inputField ? inputField.innerText : "";

        if (messageText.trim() === "") {
            console.warn("GUARD: Leere Nachricht ignoriert.");
            return;
        }

        // 4. ERST die gespeicherte tenant_id aus dem Speicher holen
        chrome.storage.local.get(['tenant_id'], (result) => {
            const currentTenantId = result.tenant_id || "unknown_user";
            console.log("GUARD: Prüfung läuft für User:", currentTenantId);

            // 5. Nachricht an background.js senden (inklusive der ID!)
            chrome.runtime.sendMessage({ 
                type: "VERIFY_CONTENT", 
                text: messageText,
                tenant_id: currentTenantId 
            }, (response) => {
                
                if (response && response.is_sensitive) {
                    // FALL: Gefährlicher Inhalt
                    console.error("GUARD: Blockiert! Sensitive Daten für Tenant:", currentTenantId);
                    alert("🛑 GEMINI GUARD WARNUNG:\n\nIn deiner Nachricht wurden sensible Daten gefunden. Der Vorgang wurde gemeldet.");
                    
                    // Hinweis: Dein Backend hat nun bereits die ID und den Text erhalten 
                    // und kann die RISKY_MESSAGE Aktion serverseitig auslösen.
                } 
                else if (response && response.is_sensitive === false) {
                    // FALL: Alles okay
                    console.log("GUARD: Nachricht sicher. Sende...");
                    btn.dataset.checked = "true"; 
                    btn.click(); // Programmatischer Klick zum Absenden
                } 
                else {
                    // FALL: Fehler (z.B. Backend offline)
                    console.error("GUARD: Sicherheitscheck fehlgeschlagen.");
                    alert("⚠️ Fehler: Die Sicherheitsprüfung ist aktuell nicht erreichbar.");
                }
            });
        });
    }, true);
}

initGuard();