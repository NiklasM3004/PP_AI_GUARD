import json
from WS_MSG_AUTH.utils.auth_utils import exchange_code_for_user_data

COGNITO_CONFIG = {
    "cognito_domain": "https://eu-north-1g1i0jhwpy.auth.eu-north-1.amazoncognito.com",
    "client_id": "5ojllet2bpdippg32toukn0e3b",
    "client_secret": "66cn5f8meqd5g1t3o6mesuunjrr8mf9rmi442vnnv98gfo9vlj",
    "redirect_uri": "http://localhost:4200"
}

async def auth_code_to_all(websocket, auth_code):
    """Verarbeitet den Auth-Code und sendet Erfolg oder Fehler an das Frontend."""
    print(f"--- AUTH-CODE EMPFANGEN ---\nCode: {auth_code}\n---------------------------")
    
    try:
        # User Daten holen
        user_info = exchange_code_for_user_data(auth_code, COGNITO_CONFIG)
        sub_id = user_info["tenant_id"]
        email = user_info["email"]

        # Erfolg an Frontend senden
        await websocket.send(json.dumps({
            "message_type": "AUTH_SUCCESS",
            "payload": {"sub_id": sub_id, "email": email}
        }))
        
    except Exception as e:
        print(f"❌ AUTH-FEHLER: {e}")
        await websocket.send(json.dumps({
            "message_type": "ERROR", 
            "message": "Login fehlgeschlagen"
        }))