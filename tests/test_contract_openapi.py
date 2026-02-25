from fastapi.testclient import TestClient
from app.main import create_app

client = TestClient(create_app())

def test_openapi_has_expected_paths():
    spec = client.get("/openapi.json").json()
    paths = spec["paths"].keys()
    assert "/" in paths
    assert "/healthz" in paths
    assert "/items" in paths
    assert "/items/{item_id}" in paths

def test_openapi_item_schema_shape():
    spec = client.get("/openapi.json").json()
    schemas = spec["components"]["schemas"]
    assert "Item" in schemas
    props = schemas["Item"]["properties"]
    # Contract expectations:
    assert set(["id", "name", "price"]).issubset(props.keys())
    assert props["id"]["type"] == "integer"
    assert props["name"]["type"] == "string"
    assert props["price"]["type"] in ("number", "integer")
