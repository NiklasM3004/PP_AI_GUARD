import pytest
import mongomock
from unittest.mock import patch
import DB_SERVICE

@pytest.fixture
def mocked_api():
    """Setup: Erstellt einen In-Memory Client für alle Tests."""
    with patch("pymongo.MongoClient", mongomock.MongoClient):
        DB_SERVICE.init("mongodb://localhost:27017")
        # Wir legen einen Test-User an, damit identify_tenant funktioniert
        DB_SERVICE.db["users"].insert_one({
            "sub_id": "user-123",
            "tenant_id": "tenant_abc_99"
        })
        yield DB_SERVICE.client

def test_identify_tenant(mocked_api):
    tid = DB_SERVICE.identify_tenant_id_by_sub_id("user-123")
    assert tid == "tenant_abc_99"

def test_add_flexible_document(mocked_api):
    # Testet die Flexibilität mit beliebigen Feldern
    DB_SERVICE.add_new_document(
        "tenant_abc_99", 
        email="test@web.de", 
        level="admin", 
        score=42
    )
    
    # Verifikation in der dynamischen DB
    doc = DB_SERVICE.client["db_tenant_abc_99"]["data"].find_one({"email": "test@web.de"})
    assert doc["level"] == "admin"
    assert doc["score"] == 42

def test_store_risky_message_flow(mocked_api):
    # Der komplette Flow: Sub_id -> Tenant_id -> Nachricht speichern
    success = DB_SERVICE.store_risky_message("user-123", "Gefährlicher Login-Versuch!")
    
    assert success is True
    # Prüfen, ob es in der richtigen Tenant-DB gelandet ist
    tenant_db = DB_SERVICE.client["db_tenant_abc_99"]
    saved_msg = tenant_db["data"].find_one({"type": "risky"})
    assert saved_msg["message"] == "Gefährlicher Login-Versuch!"
    assert saved_msg["sub_id"] == "user-123"