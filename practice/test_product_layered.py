# =====================================================

# FILE: test_product_layered.py

# =====================================================

import pytest
from product_app_layered_debug import create_app

@pytest.fixture
def client():
app = create_app()
return app.test_client()

def get_token(client):
res = client.post("/login")
return res.get_json()["access_token"]

# ---------------------------

# ADD PRODUCT

# ---------------------------

def test_add_product(client):
token = get_token(client)

```
res = client.post(
    "/api/v1/products/add",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": "Phone", "price": 1000}
)

assert res.status_code == 201
```

# ---------------------------

# LIST PRODUCTS

# ---------------------------

def test_list_products(client):
res = client.get("/api/v1/products/list")
assert res.status_code == 200

# ---------------------------

# ADD VARIANT

# ---------------------------

def test_add_variant(client):
token = get_token(client)

```
p = client.post(
    "/api/v1/products/add",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": "Shirt", "price": 500}
).get_json()

pid = p["id"]

res = client.post(
    f"/api/v1/products/{pid}/variants",
    headers={"Authorization": f"Bearer {token}"},
    json={"color": "red", "stock": 10}
)

assert res.status_code == 201
```

# ---------------------------

# STOCK DECREASE

# ---------------------------

def test_decrease_stock(client):
token = get_token(client)

```
p = client.post(
    "/api/v1/products/add",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": "Shoes", "price": 200}
).get_json()

pid = p["id"]

v = client.post(
    f"/api/v1/products/{pid}/variants",
    headers={"Authorization": f"Bearer {token}"},
    json={"color": "black", "stock": 5}
).get_json()

res = client.post(
    "/api/v1/products/decrease-stock",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "items": [
            {
                "variant_id": v["variant_id"],
                "quantity": 2
            }
        ]
    }
)

assert res.status_code == 200
```

# ---------------------------

# INSUFFICIENT STOCK

# ---------------------------

def test_insufficient_stock(client):
token = get_token(client)

```
p = client.post(
    "/api/v1/products/add",
    headers={"Authorization": f"Bearer {token}"},
    json={"name": "Watch", "price": 300}
).get_json()

pid = p["id"]

v = client.post(
    f"/api/v1/products/{pid}/variants",
    headers={"Authorization": f"Bearer {token}"},
    json={"color": "blue", "stock": 1}
).get_json()

res = client.post(
    "/api/v1/products/decrease-stock",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "items": [
            {
                "variant_id": v["variant_id"],
                "quantity": 5
            }
        ]
    }
)

assert res.status_code == 400
```
