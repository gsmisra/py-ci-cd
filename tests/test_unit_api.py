from fastapi.testclient import TestClient
from app.main import create_app

client = TestClient(create_app())

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello from FastAPI"}

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_and_get_item():
    create = client.post("/items", json={"name": "apple", "price": 1.25})
    assert create.status_code == 201
    body = create.json()
    assert body["name"] == "apple"
    assert body["price"] == 1.25
    assert "id" in body

    item_id = body["id"]
    get_r = client.get(f"/items/{item_id}")
    assert get_r.status_code == 200
    assert get_r.json() == body

def test_delete_item():
    create = client.post("/items", json={"name": "banana", "price": 2.0})
    item_id = create.json()["id"]

    del_r = client.delete(f"/items/{item_id}")
    assert del_r.status_code == 204

    get_r = client.get(f"/items/{item_id}")
    assert get_r.status_code == 404