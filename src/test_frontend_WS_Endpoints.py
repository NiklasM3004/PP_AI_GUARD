import asyncio
import json
import websockets

# Deine Test-Daten
TEST_USER = {
    "sub_id": "c0cc392c-f011-7051-a4b1-b92175662319",
    "email": "neue-mail@web.de",
    "tenant_id": "tenant_mock_99",
    "user_level": "admin"
}

async def run_test():
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        print("--- 1. Test: Authentifizierung ---")
        # Wir simulieren den AUTH-Schritt
        auth_msg = {
            "message_type": "AUTHENTICATE",
            "message": "MOCK_AUTH_CODE_123"
        }
        await websocket.send(json.dumps(auth_msg))
        # Wir warten kurz auf die Antwort (AUTH_SUCCESS)
        response = await websocket.recv()
        print(f"Server Antwort: {response}\n")

        print("--- 2. Test: Admin Daten Abfrage (MongoDB Pull) ---")
        # Hier nutzen wir deine bereitgestellten IDs
        data_request = {
            "message_type": "GET_USER_DATA",
            "tenant_id": TEST_USER["tenant_id"],
            "sub_id": TEST_USER["sub_id"]
        }
        await websocket.send(json.dumps(data_request))
        
        # Antwort vom Backend (Entweder DASHBOARD_DATA oder THX_PAGE)
        response = await websocket.recv()
        data = json.loads(response)
        
        if data["message_type"] == "DASHBOARD_DATA":
            print("✅ Erfolg: Admin-Daten wurden korrekt gepullt.")
            print(f"Anzahl Datensätze: {len(data['payload'])}")
        elif data["message_type"] == "THX_PAGE":
            print("ℹ️ Info: User ist kein Admin, THX_PAGE Signal empfangen.")
        
        print("\n--- 3. Test: Risky Message ---")
        risky_msg = {
            "message_type": "RISKY_MESSAGE",
            "payload": {"action": "DELETE_TEST_DATA"}
        }
        await websocket.send(json.dumps(risky_msg))
        response = await websocket.recv()
        print(f"Risky ACK: {response}")

if __name__ == "__main__":
    asyncio.run(run_test())