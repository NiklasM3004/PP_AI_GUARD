"""
(to test how app reacts to admins or users singed in differently)
def overwrite_or_set_value_for_sub_id(sub_id, key, value):
    Setzt oder überschreibt einen Wert für eine gegebene sub_id.


def create_admin_tenant_db(sub_id)

def identify_admindb_by_sub_id(sub_id):
    Identifiziert, ob die gegebene sub_id einem Admin zugeordnet ist via routing_db

    retun tenant_id

def add_new_document(tenant_id, all possible values)
    adds all values, does not overwrite

def store_risky_message(sub_id, message):
    idenfity_admin_db_by_sub_id(sub_id) -> tenant_id
    add_new_document(tenant_id, message)


"""



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

import pymongo
from datetime import datetime

MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "auth_routing"

client = None
db = None

def init(uri=MONGO_URI):
    global client, db
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
    db = client[DB_NAME]

def create_tenant_db(sub_id):
    """
    Erstellt theoretisch eine neue DB (in Mongo geschieht dies beim ersten Insert).
    Hier geben wir das DB-Objekt zurück.
    """
    db_name = f"tenant_{sub_id.replace('-', '_')}"
    return client[db_name]

def identify_tenant_id_by_sub_id(sub_id):
    """Sucht die tenant_id in der zentralen 'users' Collection."""
    user = db["users"].find_one({"sub_id": sub_id})
    return user.get("tenant_id") if user else None

def add_new_document(tenant_id, **fields):
    """
    Fügt einem Tenant-Dokument beliebige Felder hinzu.
    Nutzt **kwargs für maximale Flexibilität.
    """
    target_db = client[f"db_{tenant_id}"] # Dynamische DB Wahl
    payload = {**fields, "updated_at": datetime.now()}
    return target_db["data"].insert_one(payload)

def store_risky_message(sub_id, message_content):
    """
    Kombiniert die Logik: Identifiziert den Tenant und speichert eine Nachricht.
    """
    tenant_id = identify_tenant_id_by_sub_id(sub_id)
    if not tenant_id:
        print(f"⚠️ Kein Tenant für sub_id {sub_id} gefunden.")
        return False
    
    # Speichert die Nachricht mit der sub_id als Absender-Info
    add_new_document(tenant_id, sub_id=sub_id, message=message_content, type="risky")
    return True

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