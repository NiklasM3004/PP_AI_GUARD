# 1. Navigiere zum Download-Ordner (wo die Dateien liegen)
cd ~/Downloads

# 2. Tool ausführbar machen
chmod +x ai_security_redteam.py

# 3. Test-Modus starten (zeigt Beispiele)
python3 ai_security_redteam.py --test

# 4. Interaktiven Modus starten
python3 ai_security_redteam.py

# 5. Einzelnen Text direkt scannen
python3 ai_security_redteam.py "Meine Email ist test@firma.de"
```

## Im interaktiven Modus dann:
```
# Beispiele zum Ausprobieren:
"Kannst du mir helfen?"  → Sicher ✅

"Meine Email ist max@firma.de"  → Warnung 🟠

"API Key: sk_live_abc123xyz"  → Kritisch 🔴

"quit"  → Beenden