import boto3
import sys

# --- KONFIGURATION ---
REGION = "eu-north-1" # Deine Region, z.B. eu-central-1
CLIENT_ID = "5ojllet2bpdippg32toukn0e3b" # Deine App Client ID

# Initialisierung des AWS Clients
client = boto3.client('cognito-idp', region_name=REGION)

def register_user(email, password):
    print(f"\n--- Starte Registrierung für: {email} ---")
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                # Falls du custom attributes hast, hier hinzufügen:
                # {'Name': 'custom:role', 'Value': 'admin'}
            ]
        )
        print("✅ ERFOLG: User wurde angelegt.")
        print(f"AWS Rückmeldung: UserSub = {response['UserSub']}")
        print("Schau jetzt in deine AWS Console unter 'User Pools' nach!")
        
    except client.exceptions.UsernameExistsException:
        print("❌ FEHLER: Dieser User existiert bereits.")
    except Exception as e:
        print(f"❌ FEHLER: {str(e)}")

if __name__ == "__main__":
    # Test-Daten (ändere diese zum Testen)
    test_email = "test-user@beispiel.de"
    test_password = "Password123!" # Muss meist Großbuchstabe, Zahl & Sonderzeichen enthalten

    if CLIENT_ID == "DEINE_ID":
        print("Bitte trage zuerst deine CLIENT_ID im Code ein!")
        sys.exit()

    register_user(test_email, test_password)