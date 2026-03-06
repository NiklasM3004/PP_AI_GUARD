// Paste this into console to assure that extension is running

const testBtn = document.querySelector('button[aria-label*="senden"]') || document.querySelector('.send-button-container button');
if (testBtn) {
    console.log("ERFOLG: Button wurde erkannt!", testBtn);
    testBtn.style.outline = "5px solid green"; // Umrandet den Button grün
} else {
    console.log("Immer noch kein Treffer. Bitte klicke den Button rechts an -> 'Untersuchen' und schicke mir das HTML.");
}