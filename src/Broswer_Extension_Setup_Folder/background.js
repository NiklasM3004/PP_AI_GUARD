chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "VERIFY_CONTENT") {
        fetch("http://localhost:5000/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                text: request.text, 
                tenant_id: request.tenant_id // Die ID wird zum Server durchgereicht
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_sensitive) {
                // Professioneller Ansatz: Das Backend sollte den Vorfall 
                // direkt speichern, wenn is_sensitive erkannt wird.
                console.warn(`Risky Message von ${request.tenant_id} erkannt.`);
            }
            sendResponse(data);
        })    
        .catch(error => sendResponse({ error: error.message }));
        return true; // Hält den Channel für asynchrone Antwort offen
    }
});

chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
    if (request.type === "SAVE_TENANT") {
        console.log("ID von Webseite empfangen:", request.id);
        
        // Speichere die ID im lokalen Speicher der Extension
        chrome.storage.local.set({ "tenant_id": request.id }, () => {
            sendResponse({ success: true, message: "ID gespeichert" });
        });
        return true; // Hält den Channel für die Antwort offen
    }
});