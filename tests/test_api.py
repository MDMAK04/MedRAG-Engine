from unittest.mock import patch, MagicMock

# On simule que Qdrant et le modèle sont "connectés" avant d'importer l'app
with patch("backend.services.pdf_ingestion.QdrantClient", return_value=MagicMock()):
    with patch("backend.services.pdf_ingestion.SentenceTransformer", return_value=MagicMock()):
        from backend.main import app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MedIntel-AI API is running"}