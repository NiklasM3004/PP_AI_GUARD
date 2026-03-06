import requests

# Test-Szenarien: (Text, Erwartetes Ergebnis: True = Sensitiv, False = OK)
test_cases = [
    # --- POSITIV-TESTS (Sollten True ergeben) ---
    ("Kontakt: max.mustermann@web.de", True),                # Email
    ("Zahlung per 4512-4512-4512-4512", True),               # Credit Card
    ("Meine SSN ist 123-45-6789", True),                     # SSN
    ("Ruf mich an: +49 170 1234567", True),                  # Phone
    ("API_KEY: 'AKIAIOSFODNN7EXAMPLE'", True),               # API Key
    ("Login mit password='supersecret123'", True),           # Password
    ("Server IP ist 192.168.178.1", True),                   # IP
    ("Datei liegt unter C:\\Users\\Admin\\Desktop\\geheim.txt", True), # Path Windows
    ("Log unter /home/user/logs/app.log", True),             # Path Linux/Mac
    
    # --- NEGATIV-TESTS (Sollten False ergeben) ---
    ("Hallo, wie geht es dir?", False),                      # Normaler Text
    ("Das kostet 12,99€", False),                            # Zahlen ohne Pattern
    ("Die Versionsnummer ist 1.2.3", False),                 # Ähnlich wie IP, aber kürzer
    ("Ich wohne in der Hauptstraße 5", False),               # Adresse ohne Pattern-Match
    ("Vielen Dank für Ihre Nachricht. Sie erreichen mich jederzeit unter meiner E-Mail-Adresse max.mustermann@web.de für weitere Rückfragen.", True),
    ("Die Abbuchung erfolgt automatisch von Ihrer hinterlegten Kreditkarte mit der Endnummer 4512-4512-4512-4512 am Ersten des Monats.", True),
    ("Für die Steuererklärung benötige ich noch Ihre Sozialversicherungsnummer, die im Format 123-45-6789 vorliegen sollte.", True),
    ("Falls Sie technische Probleme haben, rufen Sie bitte unseren Support unter +49 170 1234567 an, wir helfen Ihnen gerne weiter.", True),
    ("Um die Integration abzuschließen, kopieren Sie den API_KEY: 'AKIAIOSFODNN7EXAMPLE' in Ihre Konfigurationsdatei.", True),
    ("Ihr temporärer Zugang wurde eingerichtet. Bitte nutzen Sie das Passwort password='supersecret123' für den ersten Login.", True),
    ("Der Datenbankserver ist intern über die IP-Adresse 192.168.178.1 erreichbar, bitte prüfen Sie die Firewall-Einstellungen.", True),
    ("Ich habe das Dokument lokal unter C:\\Users\\Admin\\Desktop\\geheim.txt gespeichert und werde es später hochladen.", True),
    ("Die Log-Dateien des Webservers befinden sich im Verzeichnis /home/user/logs/app.log und können mit 'tail' eingesehen werden.", True),

    # --- NEGATIV-TESTS (Sollten False ergeben) ---
    ("Das ist ein ganz normaler Satz ohne jegliche sensiblen Informationen, der einfach nur so hier steht.", False),
    ("Die Temperatur beträgt heute 22 Grad Celsius und es ist leicht bewölkt in Berlin.", False),
    ("Bitte senden Sie das Paket an die Packstation 123 in 12345 Musterstadt.", False), 
    ("Die Version 2.0.4 des Programms wurde gestern erfolgreich auf dem Staging-System deployed.", False),("Vielen Dank für Ihre Nachricht. Sie erreichen mich jederzeit unter meiner E-Mail-Adresse max.mustermann@web.de für weitere Rückfragen.", True),
    ("Die Abbuchung erfolgt automatisch von Ihrer hinterlegten Kreditkarte mit der Endnummer 4512-4512-4512-4512 am Ersten des Monats.", True),
    ("Für die Steuererklärung benötige ich noch Ihre Sozialversicherungsnummer, die im Format 123-45-6789 vorliegen sollte.", True),
    ("Falls Sie technische Probleme haben, rufen Sie bitte unseren Support unter +49 170 1234567 an, wir helfen Ihnen gerne weiter.", True),
    ("Um die Integration abzuschließen, kopieren Sie den API_KEY: 'AKIAIOSFODNN7EXAMPLE' in Ihre Konfigurationsdatei.", True),
    ("Ihr temporärer Zugang wurde eingerichtet. Bitte nutzen Sie das Passwort password='supersecret123' für den ersten Login.", True),
    ("Der Datenbankserver ist intern über die IP-Adresse 192.168.178.1 erreichbar, bitte prüfen Sie die Firewall-Einstellungen.", True),
    ("Ich habe das Dokument lokal unter C:\\Users\\Admin\\Desktop\\geheim.txt gespeichert und werde es später hochladen.", True),
    ("Die Log-Dateien des Webservers befinden sich im Verzeichnis /home/user/logs/app.log und können mit 'tail' eingesehen werden.", True),

    # --- NEGATIV-TESTS (Sollten False ergeben) ---
    ("Das ist ein ganz normaler Satz ohne jegliche sensiblen Informationen, der einfach nur so hier steht.", False),
    ("Die Temperatur beträgt heute 22 Grad Celsius und es ist leicht bewölkt in Berlin.", False),
    ("Bitte senden Sie das Paket an die Packstation 123 in 12345 Musterstadt.", False), 
    ("Die Version 2.0.4 des Programms wurde gestern erfolgreich auf dem Staging-System deployed.", False),
    # --- NEUE PATTERNS (POSITIV) ---
    ("Überweisen Sie das Geld auf DE21100200300012345678.", True),     # IBAN
    ("Hardware-ID: 00:1A:2B:3C:4D:5E", True),                          # MAC
    ("Mein Geburtsdatum ist der 15.03.1992.", True),                    # Geburtsdatum
    ("Sende die BTC an 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", True),     # Bitcoin
    ("Hier ist mein Schlüssel: -----BEGIN RSA PRIVATE KEY-----", True), # Private Key
    
    # --- NEUE PATTERNS (NEGATIV - SOLLTEN OK SEIN) ---
    ("Die IBAN fängt in Deutschland mit DE an.", False),               # Zu kurz
    ("Die Versionsnummer ist 2.1.0.", False),                          # Kein Geburtsdatum
    ("Treffen wir uns am 12.12. um 14 Uhr?", False),                   # Unvollständiges Datum
    ("Der Wert liegt bei 1.234.567,89 Euro.", False),                  # Tausender-Trennzeichen
]

def run_tests():
    print(f"{'TESTFALL':<45} | {'ERGEBNIS':<12} | {'STATUS'}")
    print("-" * 75)
    
    for text, expected in test_cases:
        try:
            response = requests.post("http://localhost:5000/check", json={"text": text})
            res_data = response.json()
            actual = res_data['is_sensitive']
            
            # Erfolgskontrolle
            status = "✅ PASS" if actual == expected else "❌ FAIL"
            
            display_text = text if len(text) < 45 else text[:42] + "..."
            print(f"{display_text:<45} | {str(actual):<12} | {status}")
            
        except Exception as e:
            print(f"Fehler: Server läuft wahrscheinlich nicht. {e}")
            break

if __name__ == "__main__":
    run_tests()