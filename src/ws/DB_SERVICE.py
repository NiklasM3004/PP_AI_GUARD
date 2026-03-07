import pymongo
from datetime import datetime
import json

# Konfiguration (Später in .env auslagern)
MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "auth_routing"

client = None
db = None

def init():
    """Initialisiert die Verbindung und führt einen Health-Check aus."""
    global client, db
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        client.admin.command('ping') # Health-Check
        print("✅ MongoDB Health-Check: Verbindung steht.")
    except Exception as e:
        print(f"❌ MongoDB Fehler: {e}")

def save_test_account_data(tenant_id, data_list):
    """Speichert eine Liste von virtuellen Account-Daten."""
    if db is None: return
    collection = db["test_accounts"]
    # Speichert Daten mit Timestamp
    payload = {"tenant_id": tenant_id, "data": data_list, "created_at": datetime.now()}
    collection.update_one({"tenant_id": tenant_id}, {"$set": payload}, upsert=True)

async def getsensitive_messages_list(websocket, sub_id):
    """Prüft Level und sendet entweder Daten oder triggert die THX-PAGE."""
    # Simulierter Level-Check (Hier käme normalerweise ein DB-Query)
    is_admin = db["users"].find_one({"sub_id": sub_id, "role": "admin"}) is not None
    
    if is_admin:
        # Pull alle Messages und Print im Terminal
        all_data = list(db["test_accounts"].find({}, {"_id": 0}))
        print(f"--- ADMIN PULL für {sub_id} ---\n{all_data}\n----------------")
        await websocket.send(json.dumps({"message_type": "DASHBOARD_DATA", "payload": all_data}))
    else:
        # Einzeiler-Logik für das Frontend
        await websocket.send(json.dumps({"message_type": "THX_PAGE", "payload": "Normal User Redirect"}))