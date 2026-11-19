from fastapi.testclient import TestClient
from app.main import app

def test_authoritative_dataset_catalogue_is_exposed():
    response=TestClient(app).get("/api/datasets")
    assert response.status_code==200
    payload=response.json()
    assert payload["count"]>=8
    assert all(item["download_url"].startswith("https://") for item in payload["datasets"])
    assert {item["provider"] for item in payload["datasets"]} >= {"Our World in Data","World Bank"}

def test_unknown_dataset_preview_is_rejected():
    response=TestClient(app).get("/api/datasets/not-a-real-dataset/preview")
    assert response.status_code==404
