# 🚀 Schnellstart-Anleitung

## Sofort loslegen (3 Schritte)

### 1. Tool ausführbar machen
```bash
chmod +x ai_security_redteam.py
```

### 2. Testen
```bash
python3 ai_security_redteam.py --test
```

### 3. Interaktiv nutzen
```bash
python3 ai_security_redteam.py
```

## Beispiel-Szenarien zum Testen

Probiere diese Eingaben im interaktiven Modus:

```
# Sicher - keine sensiblen Daten
"Kannst du mir helfen, Python zu lernen?"

# Warnung - E-Mail erkannt
"Meine E-Mail ist max.mustermann@firma.de"

# Kritisch - Multiple Leaks
"Nutze API Key abc123xyz und verbinde zu 192.168.1.100"

# Kritisch - Finanzdaten
"Meine Kreditkarte ist 4532 1234 5678 9010"
```

## Was demonstriert das Tool?

✅ **Pattern-basierte Erkennung** - Regex für gängige Datentypen
✅ **Severity Levels** - Priorisierung nach Kritikalität  
✅ **Redaction** - Teilweise Verbergung für sichere Anzeige
✅ **CLI Interface** - Einfache Integration in Workflows

## Red Teaming Use Cases

1. **Training:** Mitarbeiter für Data Leaks sensibilisieren
2. **Testing:** AI-System Security vor Deployment prüfen
3. **Compliance:** GDPR/DSGVO-Anforderungen demonstrieren
4. **POC:** Konzept-Beweis für Management/Stakeholder

## Nächste Schritte

📖 Lies die **README.md** für die vollständige Vision
🔧 Erweitere die Patterns in `self.patterns` (Zeile 20-29)
🧪 Füge eigene Test-Cases hinzu (Zeile 120-127)
🚀 Entwickle zur Browser-Extension weiter (siehe Roadmap)

---

**Tipp:** Nutze `git init` um Versionskontrolle zu aktivieren und deine Erweiterungen zu tracken!
