#!/usr/bin/env python3
"""
Startet Test-Chat-Seite automatisch im Browser
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Port für den Server
PORT = 8001

# Finde test_chat.html
current_dir = Path(__file__).parent
html_file = current_dir / "check_browser_button.html"

if not html_file.exists():
    print(f"❌ Fehler: test_chat.html nicht gefunden in {current_dir}")
    exit(1)

print("=" * 60)
print("  🧪 AI Security Guard - Test-Seite Starter")
print("=" * 60)
print(f"\n✅ HTML-Datei gefunden: {html_file}")
print(f"🚀 Starte HTTP Server auf Port {PORT}...")

# Wechsle in das Verzeichnis mit der HTML-Datei
os.chdir(current_dir)

# HTTP Server starten
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/check_browser_button.html"
    
    print(f"✅ Server läuft!")
    print(f"🌐 URL: {url}")
    print(f"\n💡 Öffne Browser automatisch...")
    
    # Browser automatisch öffnen
    webbrowser.open(url)
    
    print(f"\n✅ Browser geöffnet!")
    print(f"📝 Drücke Ctrl+C zum Beenden\n")
    print("=" * 60 + "\n")
    
    # Server läuft bis Ctrl+C
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server gestoppt. Auf Wiedersehen!")
