chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "VERIFY_CONTENT") {
        fetch("http://localhost:5000/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: request.text })
        })
        .then(response => response.json())
        .then(data => sendResponse(data))
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