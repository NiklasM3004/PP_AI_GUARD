# 🚀 AI Security Guard - Installations- & Nutzungsanleitung

## 📦 Was du bekommen hast

```
project/
├── test_chat.html              # Test-Chat-Seite (lokale Demo)
├── extension/                  # Browser Extension
│   ├── manifest.json          # Extension-Konfiguration
│   ├── content.js             # Haupt-Detection-Script
│   ├── background.js          # Background Service Worker
│   ├── popup.html             # Extension-Popup UI
│   ├── popup.js               # Popup-Logic
│   └── icons/                 # Icon-Dateien
│       ├── icon.svg           # SVG Source
│       └── create_icons.sh    # Icon-Generator Script
```

---

## 🎯 SCHRITT 1: Test-Seite starten

### Option A: Einfacher HTTP Server (Python)
```bash
cd ~/Downloads  # oder wo auch immer die Dateien liegen

# Python 3 (empfohlen)
python3 -m http.server 8000

# Oder Python 2
python -m SimpleHTTPServer 8000
```

### Option B: Live Server (VS Code)
```
1. Öffne test_chat.html in VS Code
2. Rechtsklick → "Open with Live Server"
```

### Zugriff
Öffne im Browser: **http://localhost:8000/test_chat.html**

✅ Du solltest eine hübsche Chat-Oberfläche sehen!

---

## 🔧 SCHRITT 2: Extension Icons erstellen

**Problem:** Chrome Extensions brauchen PNG Icons (16x16, 48x48, 128x128)

### Schnelle Lösung: Online Converter
```
1. Gehe zu: https://cloudconvert.com/svg-to-png
2. Upload: extension/icons/icon.svg
3. Konvertiere zu PNG in 3 Größen:
   - 16x16 → speichere als icon16.png
   - 48x48 → speichere als icon48.png  
   - 128x128 → speichere als icon128.png
4. Lege alle 3 PNGs in extension/icons/
```

### Alternative: ImageMagick (wenn installiert)
```bash
cd extension/icons/

convert -background none icon.svg -resize 16x16 icon16.png
convert -background none icon.svg -resize 48x48 icon48.png
convert -background none icon.svg -resize 128x128 icon128.png
```

### Notfall-Lösung: Emoji als Icon
Wenn Icons fehlen, erstelle einfache PNGs:
```bash
# Erstelle placeholder icons (macOS/Linux)
cd extension/icons/
convert -size 128x128 xc:purple -pointsize 80 -fill white -gravity center -annotate +0+0 "🛡" icon128.png
convert icon128.png -resize 48x48 icon48.png
convert icon128.png -resize 16x16 icon16.png
```

---

## 🌐 SCHRITT 3: Extension in Chrome laden

### 1. Chrome Developer Mode aktivieren
```
1. Öffne Chrome
2. Gehe zu: chrome://extensions/
3. Aktiviere "Entwicklermodus" (oben rechts)
```

### 2. Extension laden
```
4. Klicke "Entpackte Erweiterung laden"
5. Wähle den "extension" Ordner aus
6. ✅ Extension erscheint in der Liste!
```

### 3. Extension Icon anpinnen
```
7. Klicke auf das Puzzle-Icon in Chrome (neben der Adressleiste)
8. Finde "AI Security Guard"
9. Klicke auf das Pin-Icon
```

---

## 🧪 SCHRITT 4: Testen!

### Test 1: Test-Seite
```
1. Öffne: http://localhost:8000/test_chat.html
2. Öffne Chrome DevTools (F12 oder Cmd+Option+I)
3. Gehe zum "Console" Tab
4. Du solltest sehen: "🛡️ AI Security Guard Extension geladen!"
```

### Test 2: Send-Button Detection
```
5. Schreibe etwas in das Textfeld: "Hallo Test"
6. Klicke "Senden 🚀"
7. In der Console siehst du:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🚀 SEND-BUTTON WURDE GEDRÜCKT!
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📍 Plattform: Test Chat
   📝 Text-Länge: 10 Zeichen
   📄 Inhalt: Hallo Test
```

### Test 3: Extension Popup
```
8. Klicke auf das Extension-Icon
9. Du siehst:
   - Status: Aktiv & Geschützt
   - Erkannte Clicks: 1
   - Aktuelle Seite: 🧪 Test Chat
```

---

## 🎯 SCHRITT 5: Echte LLMs testen (Optional)

Die Extension funktioniert bereits auf:
- ✅ **Claude.ai** - https://claude.ai
- ✅ **ChatGPT** - https://chat.openai.com
- ✅ **Gemini** - https://gemini.google.com
- ✅ **Copilot** - https://copilot.microsoft.com

### Testen auf Claude.ai:
```
1. Gehe zu https://claude.ai
2. Öffne Console (F12)
3. Schreibe eine Nachricht
4. Klicke Send
5. Console zeigt: "🚀 SEND-BUTTON WURDE GEDRÜCKT!"
```

**Hinweis:** Auf manchen Seiten kann es 1-2 Sekunden dauern, bis die Extension die Buttons findet (SPAs laden dynamisch).

---

## 🐛 Troubleshooting

### Problem: "Extension geladen" erscheint nicht in Console
**Lösung:**
```
1. Prüfe ob Extension aktiviert ist (chrome://extensions/)
2. Stelle sicher, dass localhost in den "matches" ist
3. Reload die Seite (Cmd+R oder F5)
4. Prüfe ob es Fehler im Extension-Tab gibt
```

### Problem: Button-Click wird nicht erkannt
**Lösung:**
```
1. Öffne Console
2. Tippe: document.querySelector('#send-button')
3. Sollte das Button-Element zeigen
4. Falls null: Prüfe HTML-Struktur
```

### Problem: Icons fehlen bei Extension-Installation
**Lösung:**
```
1. Extension funktioniert trotzdem!
2. Icons sind nur kosmetisch
3. Erstelle sie später mit dem Online-Converter
```

### Problem: "Content script failed to load"
**Lösung:**
```
1. Prüfe manifest.json auf Syntax-Fehler
2. Stelle sicher alle .js Dateien existieren
3. Chrome Extensions Page → Details → "Fehler" anzeigen
```

---

## 📊 Was die Extension macht (aktuell)

### ✅ Implementiert:
- 🔍 Erkennt Send-Buttons auf Test-Seite
- 🔍 Erkennt Send-Buttons auf Claude, ChatGPT, Gemini, Copilot
- 📝 Extrahiert Text aus Textareas
- 📊 Logged alle Button-Clicks in Console
- 🎨 Schönes Popup mit Statistiken
- ⚡ Funktioniert auf Single-Page-Apps (SPAs)

### 🔜 Kommt als nächstes (Phase 2):
- 🛡️ Integration mit Python Security Scanner
- 🚫 Blockierung bei CRITICAL Violations
- ⚠️ Visual Warnings im UI
- 📈 Erweiterte Statistiken
- ⚙️ Einstellungs-Panel

---

## 🎓 Lern-Tipps für Entwicklung

### Console Debugging:
```javascript
// In Browser Console testen:
document.querySelector('#send-button')  // Button finden
document.querySelector('#chat-input').value  // Text auslesen
```

### Extension Debugging:
```
1. chrome://extensions/
2. Details bei "AI Security Guard"
3. "Hintergrundseite untersuchen" → Service Worker Console
4. "Fehler" Tab → zeigt alle JavaScript-Fehler
```

### Content Script Testen:
```javascript
// Direkt in Page Console:
chrome.runtime.sendMessage({type: 'TEST'}, (response) => {
  console.log('Response:', response);
});
```

---

## 🚀 Nächste Schritte

### Phase 2: Security Integration
```python
# Python Backend (Flask)
@app.route('/scan', methods=['POST'])
def scan_text():
    text = request.json['text']
    violations = detector.scan(text)
    return jsonify({'violations': violations})
```

### Phase 3: Blocking implementieren
```javascript
// In content.js
if (violations.some(v => v.severity === 'CRITICAL')) {
  event.preventDefault();  // BLOCK!
  showWarningModal(violations);
}
```

### Phase 4: Production Release
- Code signieren
- Chrome Web Store Upload
- Auto-Update Mechanismus
- Privacy Policy & Dokumentation

---

## 📝 Checkliste

- [ ] Test-Seite läuft auf localhost:8000
- [ ] Icons wurden erstellt (oder Notfall-Lösung)
- [ ] Extension in Chrome geladen
- [ ] Extension-Icon ist sichtbar in Toolbar
- [ ] Console zeigt "Extension geladen"
- [ ] Send-Button Click wird geloggt
- [ ] Popup öffnet und zeigt Statistiken
- [ ] Test auf echter LLM-Seite (optional)

---

## 💡 Pro-Tipps

1. **Hot Reload während Entwicklung:**
   ```
   Nach Code-Änderungen:
   chrome://extensions/ → Reload-Icon bei deiner Extension
   Dann Page reload (F5)
   ```

2. **Multi-Browser Testing:**
   - Firefox: Fast identischer Code (kleine Anpassungen)
   - Edge: Chrome-kompatibel (funktioniert sofort)
   - Safari: Braucht Xcode & Conversion

3. **Git für Version Control:**
   ```bash
   cd extension/
   git init
   git add .
   git commit -m "Initial extension with button detection"
   ```

---

## 🎉 Erfolg!

Wenn du bis hier hin alles gemacht hast, hast du:
- ✅ Eine funktionierende Browser Extension gebaut
- ✅ Button-Detection auf mehreren Plattformen implementiert
- ✅ Die Basis für ein vollständiges Security-Tool gelegt
- ✅ Praktische Erfahrung mit Chrome Extensions gesammelt

**Nächster Schritt:** Integriere das Python Security-Tool für echtes Scanning! 🛡️

---

**Fragen? Probleme?**
- Prüfe die Chrome Extension Console (chrome://extensions/)
- Schau in die Browser DevTools Console (F12)
- Teste zuerst auf der einfachen Test-Seite

**Happy Coding! 🚀**
