function initGuard() {
    // Gemini Send-Button Selector (Stand heute)
    const sendButtonSelector = 'button[aria-label="Prompt senden"]';
    
    document.addEventListener('click', async (event) => {
        const btn = event.target.closest(sendButtonSelector);
        if (!btn || btn.dataset.guarded) return;

        // Klick abfangen
        event.preventDefault();
        event.stopImmediatePropagation();

        const inputField = document.querySelector('div[contenteditable="true"]');
        const text = inputField ? inputField.innerText : "";

        console.log("Status: Prüfung läuft...", text);
        chrome.storage.local.get(['tenant_id'], (result) => {
        console.log('Abgefragte ID:', result.tenant_id);
        });

        chrome.runtime.sendMessage({ type: "VERIFY_CONTENT", text: text }, (response) => {
            if (response && response.is_sensitive) {
                console.error("Status: BLOCKIERT", response);
                alert("Sicherheitshinweis: Sensible Daten erkannt. Senden blockiert.");
            } else {
                console.log("Status: SICHER", response);
                // Markiere Button kurzzeitig als geprüft und klicke ihn erneut
                btn.dataset.guarded = "true";
                btn.click();
                setTimeout(() => delete btn.dataset.guarded, 500);
            }
        });
    }, true);
}

// Starte das Skript
initGuard();
console.log("Gemini Guard aktiv.");