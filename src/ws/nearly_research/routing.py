import uuid
from motor.motor_asyncio import AsyncIOMotorClient

# Verbindungseinstellungen (aus deiner docker-compose.local.yaml)
uri = "mongodb://admin:password@localhost:27018/"
client = AsyncIOMotorClient(uri)
collection = client["global_admin"]["user_tenant_mapping"]

async def create_admin_routing(sub_id, email):
    # 1. Generiere eine absolut einzigartige ID für die neue Mandanten-Datenbank
    # Wir nehmen einen Präfix + einen Teil einer UUID für die Lesbarkeit
    unique_tenant_id = f"tenant_{uuid.uuid4().hex[:12]}"

    # 2. Das Dokument-Template
    routing_data = {
        "sub_id": sub_id,
        "email": email,
        "tenant_id": unique_tenant_id,
        "user_level": "admin"
    }

    # 3. In die Routing-DB schreiben
    # 'upsert=True' erstellt den Eintrag, falls die sub_id noch nicht existiert
    await collection.update_one(
        {"sub_id": sub_id}, 
        {"$set": routing_data}, 
        upsert=True
    )
    
    print(f"✅ Admin-Routing erstellt: DB-Name wird '{unique_tenant_id}'")
    return unique_tenant_id