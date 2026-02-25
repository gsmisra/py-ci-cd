from fastapi import FastAPI, HTTPException
from .schemas import Item, ItemCreate

def create_app() -> FastAPI:
    app = FastAPI(title="Sample FastAPI CI/CD/CT", version="1.0.0")

    # In-memory store (demo purpose)
    db: dict[int, Item] = {}
    next_id = {"value": 1}

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/")
    def root():
        return {"message": "Hello from FastAPI"}

    @app.post("/items", response_model=Item, status_code=201)
    def create_item(payload: ItemCreate):
        item_id = next_id["value"]
        next_id["value"] += 1
        item = Item(id=item_id, **payload.model_dump())
        db[item_id] = item
        return item

    @app.get("/items/{item_id}", response_model=Item)
    def get_item(item_id: int):
        if item_id not in db:
            raise HTTPException(status_code=404, detail="Item not found")
        return db[item_id]

    @app.delete("/items/{item_id}", status_code=204)
    def delete_item(item_id: int):
        if item_id not in db:
            raise HTTPException(status_code=404, detail="Item not found")
        del db[item_id]
        return None

    return app

app = create_app()
