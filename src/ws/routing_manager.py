import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

# --- KONFIGURATION (Basierend auf deiner docker-compose.local.yaml) ---
# Wir nutzen admin:password und Port 27017
MONGO_URI = "mongodb://admin:password@localhost:27018/"
DB_NAME = "global_admin"
COLLECTION_NAME = "user_tenant_mapping"

class RoutingManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    async def check_user_exists(self, sub_id):
        """
        Prüft, ob eine sub_id existiert und ein user_level (role) hat.
        Gibt das Dokument zurück, falls gefunden, sonst None.
        """
        user = await self.collection.find_one({"sub_id": sub_id})
        if user and "user_level" in user:
            return user
        return None

    async def upsert_user(self, sub_id, email=None, tenant_id=None, user_level=None):
        """
        Schreibt Daten in die Haupt-DB. 
        Funktioniert für einzelne Werte oder alle zusammen (Update oder Insert).
        """
        # Wir bauen ein Update-Objekt nur mit den Werten, die nicht None sind
        update_data = {}
        if email: update_data["email"] = email
        if tenant_id: update_data["tenant_id"] = tenant_id
        if user_level: update_data["user_level"] = user_level

        if not update_data:
            print("Keine Daten zum Aktualisieren übergeben.")
            return

        # 'upsert=True' sorgt dafür, dass der Eintrag erstellt wird, falls er nicht existiert
        result = await self.collection.update_one(
            {"sub_id": sub_id},
            {"$set": update_data},
            upsert=True
        )
        return result

# --- TESTS ---
async def run_tests():
    manager = RoutingManager()
    test_sub_id = "c0cc392c-f011-7051-a4b1-b92175662319"
    
    print(f"--- Starte Tests für sub_id: {test_sub_id} ---")

    # Test 1: Prüfen, ob User existiert (sollte am Anfang False sein)
    exists = await manager.check_user_exists(test_sub_id)
    print(f"Test 1 (Existenz vorab): {'Gefunden' if exists else 'Nicht gefunden'} (Erwartet: Nicht gefunden)")

    # Test 2: User mit Mock-Daten anlegen
    print("Test 2: Lege Mock-Daten an...")
    await manager.upsert_user(
        sub_id=test_sub_id,
        email="test@example.com",
        tenant_id="tenant_mock_99",
        user_level="admin"
    )

    # Test 3: Erneute Prüfung nach dem Anlegen
    exists_now = await manager.check_user_exists(test_sub_id)
    if exists_now:
        print(f"Test 3 (Existenz danach): Gefunden! User-Level ist: {exists_now.get('user_level')}")
    else:
        print("Test 3 fehlgeschlagen: User wurde nicht gefunden.")

    # Test 4: Einzelnen Wert aktualisieren (nur email)
    print("Test 4: Aktualisiere nur die Email...")
    await manager.upsert_user(sub_id=test_sub_id, email="neue-mail@web.de")
    updated_user = await manager.check_user_exists(test_sub_id)
    print(f"Neue Email in DB: {updated_user.get('email')}")

if __name__ == "__main__":
    # Beachte: MongoDB Container aus docker-compose muss laufen!
    asyncio.run(run_tests())