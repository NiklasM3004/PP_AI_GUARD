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