import asyncio
import json
import websockets
from DB_SERVICE import getsensitive_messages_list
# Importiere die neue Funktion
from WS_MSG_AUTH.auth_code_to_all import auth_code_to_all

from WS_MSG_INVITE.invite_handler import handle_invite
from WS_MSG_RISKY_MESSAGE.risky_handler import handle_risky_message

MOCK_DB = {
    "c0cc392c-f011-7051-a4b1-b92175662319": ["Rasen mähen", "Einkaufen", "Python lernen"],
    "ID_MARIA": ["Projekt-Meeting", "Kaffee trinken", "Angular Updaten"]
}

async def handle_connection(websocket):
    print(f"--- Neuer Client verbunden ---")
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get("message_type")

            if msg_type == "AUTHENTICATE":
                # Hier rufen wir die ausgelagerte Logik auf
                await auth_code_to_all(websocket, data.get("message"))

            elif msg_type == "INVITE":
                await handle_invite(websocket, payload=data.get("payload")) # Einzeiler

            elif msg_type == "RISKY_MESSAGE":
                await handle_risky_message(websocket, message) # Einzeiler

            elif msg_type == "GET_WORKFLOW_LIST":
                await getsensitive_messages_list(websocket, data.get("sub_id")) # Einzeiler

    except websockets.exceptions.ConnectionClosed:
        print("[INFO] Client hat die Verbindung getrennt.")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Backend-Server läuft auf ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())