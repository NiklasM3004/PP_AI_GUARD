import boto3
import hmac
import hashlib
import base64

# --- KONFIGURATION ---
REGION = "eu-north-1"
CLIENT_ID = "5ojllet2bpdippg32toukn0e3b"
CLIENT_SECRET = "66cn5f8meqd5g1t3o6mesuunjrr8mf9rmi442vnnv98gfo9vlj" # Finde dies in der AWS Konsole

client = boto3.client('cognito-idp', region_name=REGION)

def get_secret_hash(username, client_id, client_secret):
    """Berechnet den notwendigen SecretHash für AWS Cognito"""
    message = username + client_id
    dig = hmac.new(
        str(client_secret).encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def register_user(email, password):
    print(f"\n--- Starte Registrierung für: {email} ---")
    
    # Berechne den Hash
    secret_hash = get_secret_hash(email, CLIENT_ID, CLIENT_SECRET)
    
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=secret_hash, # <--- Dies wird nun mitgesendet
            Username=email,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}]
        )
        print("✅ ERFOLG: User wurde angelegt.")
        print(f"UserSub: {response['UserSub']}")
        
    except Exception as e:
        print(f"❌ FEHLER: {str(e)}")

if __name__ == "__main__":
    register_user("test-user@beispiel.de", "Password123!")