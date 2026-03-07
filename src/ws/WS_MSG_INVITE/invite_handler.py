import json

async def handle_invite(websocket, payload):
    """Skelett für Einladungs-Logik."""
    print(f"[LOGIC] INVITE erreicht mit Payload: {payload}")
    # Anleitung für dich selbst: Hier später User-Lookup & Mail-Versand
    response = {
        "message_type": "INVITE_ACK",
        "payload": "Funktion erreicht. Sende hier tenant_id und email_to_invite."
    }
    await websocket.send(json.dumps(response))