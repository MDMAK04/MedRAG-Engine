from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MedIntel-AI API is running"}