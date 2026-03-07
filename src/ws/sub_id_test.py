import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Konfiguration aus deiner docker-compose.local.yaml
MONGO_URI = "mongodb://admin:password@localhost:27018/"
DB_NAME = "global_admin"
COLLECTION_NAME = "user_tenant_mapping"

async def does_user_exist(sub_id):
    """
    Prüft, ob für die gegebene sub_id bereits ein Routing-Eintrag existiert.
    Gibt True zurück, wenn ein Dokument gefunden wurde, sonst False.
    """
    client = AsyncIOMotorClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    # Suche nach einem Dokument mit der sub_id
    user_document = await collection.find_one({"sub_id": sub_id})
    
    # Schließe die Verbindung (optional bei Skripten, wichtig bei vielen Aufrufen)
    client.close()
    
    return user_document is not None

# --- TEST DER FUNKTION ---
async def test():
    print("--- Teste Datenbank-Check ---")
    
    # Test mit einer ID, die es wahrscheinlich nicht gibt
    fake_id = "meine-test-id-123"
    ergebnis = await does_user_exist(fake_id)
    print(f"Existiert ID '{fake_id}'? -> {ergebnis}")

if __name__ == "__main__":
    # Sicherstellen, dass der Docker-Container läuft!
    asyncio.run(test())