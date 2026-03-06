from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Erlaubt der Browser-Extension den Zugriff

PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b(?:\d{4}[-\s]?){3}\d{4}\b',                         # Credit Card
    r'\b\d{3}-\d{2}-\d{4}\b',                               # SSN
    r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', # Phone
    r'\b(?:api[_-]?key|token)[:\s]*["\']?([a-zA-Z0-9_\-]{20,})["\']?', # API Key
    r'(?:password|passwd|pwd)[:\s]*["\']?([^\s"\']{6,})["\']?',        # Password
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',                         # IP
    r'(?:[A-Z]:\\|/home/|/Users/)[\w\\/.-]+'                # Paths
    r'\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){12,30}\b',                     # IBAN
    r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b',              # MAC Address
    r'\b(?:0[1-9]|[12]\d|3[01])\.(?:0[1-9]|1[012])\.(?:19|20)\d{2}\b', # Geburtsdatum (DE)
    r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',                          # Bitcoin Adresse
    r'-----BEGIN (?:[A-Z ]+)PRIVATE KEY-----'                        # Private Key Header
]

def is_sensitive(text):
    for pattern in PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@app.route('/check', methods=['POST'])
def check_text():
    data = request.json
    text = data.get("text", "").strip()

    # LOGGING: Ausgabe im VS-Code Terminal
    if not text:
        print("---> [WARNUNG] Empfangener Text ist leer oder fehlt!")
    else:
        print(f"---> Empfangener Text: {text}")

    result = is_sensitive(text)

    status = "BLOCKIERT (Sensitiv)" if result else "FREIGEGEBEN (OK)"
    print(f"<--- Ergebnis: {status}")

    print(f"<--- Ergebnis der Prüfung: {'SENSITIV' if result else 'OK'}")
    return jsonify({"is_sensitive": result})

if __name__ == "__main__":
    print("Server läuft auf http://localhost:5000")
    app.run(port=5000)