import asyncio
import json
import websockets
import sub_id_test
from auth_utils import exchange_code_for_user_data
import routing

# 1. Unsere gemockte Datenbank
MOCK_DB = {
    "c0cc392c-f011-7051-a4b1-b92175662319": ["Rasen mähen", "Einkaufen", "Python lernen"],
    "ID_MARIA": ["Projekt-Meeting", "Kaffee trinken", "Angular Updaten"]
}

COGNITO_CONFIG = {
    "cognito_domain": "https://eu-north-1g1i0jhwpy.auth.eu-north-1.amazoncognito.com",
    "client_id": "5ojllet2bpdippg32toukn0e3b",
    "client_secret": "66cn5f8meqd5g1t3o6mesuunjrr8mf9rmi442vnnv98gfo9vlj", # Bitte in AWS Console ablesen!
    "redirect_uri": "http://localhost:4200"
}

async def handle_connection(websocket):
    print(f"--- Neuer Client verbunden ---")
    try:
        async for message in websocket:
            # Nachricht vom Frontend empfangen
            data = json.loads(message)
            msg_type = data.get("message_type")
            if msg_type == "AUTHENTICATE":
                auth_code = data.get("message")
                print(f"--- AUTH-CODE EMPFANGEN ---")
                print(f"Code: {auth_code}")
                print(f"---------------------------")
                
                try:
                    # Umwandlung via auth_utils
                    user_info = exchange_code_for_user_data(auth_code, COGNITO_CONFIG)
                    
                    sub_id = user_info["tenant_id"]
                    email = user_info["email"]
                    judge = await sub_id_test.does_user_exist(sub_id)
                    print(judge)
                    if judge is False:
                        print("registration of a new admin ...")
                        unique_tenant_id = await routing.create_admin_routing(sub_id, email)
                        # Ausgabe im Terminal wie gewünscht
                        
                        print(f"✅ ERFOLG: Nutzer identifiziert")
                        print(f"   > SUB_ID: {sub_id}")
                        print(f"   > EMAIL:  {email}\n")

                    # Bestätigung an Frontend senden
                    await websocket.send(json.dumps({
                        "message_type": "AUTH_SUCCESS",
                        "payload": {"sub_id": sub_id, "email": email}
                    }))

                except Exception as e:
                    print(f"❌ AUTH-FEHLER: {e}")
                    await websocket.send(json.dumps({"message_type": "ERROR", "message": "Login fehlgeschlagen"}))

            elif msg_type == "GET_WORKFLOW_LIST":
                t_id = data.get("tenant_id")
                print(f"[DATA] Anfrage für Liste von Tenant: {t_id}")
                user_list = MOCK_DB.get(t_id, ["Keine Daten für diese ID gefunden"])
                
                response = {
                    "message_type": "WORKFLOW_LIST_RESPONSE",
                    "payload": user_list
                }
                await websocket.send(json.dumps(response))
            
    except websockets.exceptions.ConnectionClosed:
        print("[INFO] Client hat die Verbindung getrennt.")

async def main():
    # Wir starten auf localhost Port 8765
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Backend-Server läuft auf ws://localhost:8765")
        await asyncio.Future()  # Hält den Server aktiv

if __name__ == "__main__":
    asyncio.run(main())