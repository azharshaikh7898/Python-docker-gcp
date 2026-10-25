from fastapi.testclient import TestClient
from app.main import app, ITEMS

client = TestClient(app)


def setup_function():
    ITEMS.clear()


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello from Cloud Run"}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_and_get_item():
    r = client.post("/items/1", json={"name": "pen", "price": 1.5})
    assert r.status_code == 201
    r = client.get("/items/1")
    assert r.json() == {"name": "pen", "price": 1.5}


def test_duplicate_item_conflict():
    client.post("/items/1", json={"name": "pen", "price": 1.5})
    r = client.post("/items/1", json={"name": "pen", "price": 1.5})
    assert r.status_code == 409


def test_missing_item_404():
    assert client.get("/items/999").status_code == 404
