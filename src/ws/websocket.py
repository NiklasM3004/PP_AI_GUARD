import asyncio
import json
import websockets

# 1. Unsere gemockte Datenbank
MOCK_DB = {
    "ID_PETER": ["Rasen mähen", "Einkaufen", "Python lernen"],
    "ID_MARIA": ["Projekt-Meeting", "Kaffee trinken", "Angular Updaten"]
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
                
                # Hier simulieren wir vorerst die erfolgreiche Prüfung
                # In der nächsten Stufe rufst du hier deine 'converter.py' auf
                response = {
                    "message_type": "AUTH_SUCCESS",
                    "payload": {
                        "sub_id": "ID_PETER",  # Hartkodiert zum Testen
                        "email": "test@example.com"
                    }
                }
                await websocket.send(json.dumps(response))

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