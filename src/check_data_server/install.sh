#!/bin/bash

echo "🚀 Installiere PromptGuard Server..."

# 1. App in den Programme-Ordner kopieren
sudo cp -R dist/PromptGuardServer.app /Applications/

# 2. Autostart-Datei in den LaunchAgents Ordner kopieren
mkdir -p ~/Library/LaunchAgents
cp com.promptguard.server.plist ~/Library/LaunchAgents/

# 3. Den Dienst registrieren und starten
launchctl load ~/Library/LaunchAgents/com.promptguard.server.plist

echo "✅ Installation abgeschlossen! Der Server läuft nun im Hintergrund."