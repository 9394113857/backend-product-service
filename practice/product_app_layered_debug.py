# =====================================================

# FILE: product_app_layered_debug.py

# =====================================================

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

def create_app():
app = Flask(**name**)

```
# CONFIG
app.config["JWT_SECRET_KEY"] = "test-secret"
app.config["TESTING"] = True

jwt = JWTManager(app)

# -----------------------------
# IN-MEMORY STORAGE
# -----------------------------
products = {}
variants = {}

# -----------------------------
# SERVICE FUNCTIONS
# -----------------------------
def create_product(data):
    pid = len(products) + 1
    product = {
        "id": pid,
        "name": data["name"],
        "price": data["price"],
        "variants": []
    }
    products[pid] = product
    return product

def create_variant(pid, data):
    vid = len(variants) + 1
    variant = {
        "variant_id": vid,
        "product_id": pid,
        "color": data["color"],
        "stock": data["stock"]
    }
    variants[vid] = variant
    products[pid]["variants"].append(variant)
    return variant

# -----------------------------
# ROUTES
# -----------------------------
bp = Blueprint("products", __name__)

@bp.post("/add")
@jwt_required()
def add_product():
    data = request.get_json() or {}

    if "name" not in data or "price" not in data:
        return jsonify({"message": "Missing fields"}), 400

    product = create_product(data)
    return jsonify(product), 201

@bp.get("/list")
def list_products():
    return jsonify(list(products.values())), 200

@bp.post("/<int:pid>/variants")
@jwt_required()
def add_variant(pid):
    data = request.get_json() or {}

    if pid not in products:
        return jsonify({"message": "Product not found"}), 404

    if "color" not in data or "stock" not in data:
        return jsonify({"message": "Missing fields"}), 400

    variant = create_variant(pid, data)
    return jsonify(variant), 201

@bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    for item in items:
        vid = item["variant_id"]
        qty = item["quantity"]

        if vid not in variants:
            return jsonify({"error": "Variant not found"}), 404

        if variants[vid]["stock"] < qty:
            return jsonify({"error": "Insufficient stock"}), 400

        variants[vid]["stock"] -= qty

    return jsonify({"message": "Stock decreased"}), 200

# -----------------------------
# LOGIN (FOR TESTING JWT)
# -----------------------------
@app.post("/login")
def login():
    token = create_access_token(identity="1")
    return jsonify({"access_token": token}), 200

# REGISTER BLUEPRINT
app.register_blueprint(bp, url_prefix="/api/v1/products")

return app
```

if **name** == "**main**":
app = create_app()
app.run(debug=True)
