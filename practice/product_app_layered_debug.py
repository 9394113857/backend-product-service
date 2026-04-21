from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True

    jwt = JWTManager(app)

    # In-memory storage
    products = {}
    variants = {}

    # -----------------------------
    # Services
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
    # Routes
    # -----------------------------
    bp = Blueprint("products", __name__)

    @bp.post("/add")
    @jwt_required()
    def add_product():
        data = request.get_json() or {}
        if "name" not in data or "price" not in data:
            return jsonify({"message": "Missing fields"}), 400
        return jsonify(create_product(data)), 201

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
        return jsonify(create_variant(pid, data)), 201

    @bp.post("/decrease-stock")
    @jwt_required()
    def decrease_stock():
        data = request.get_json() or {}
        for item in data.get("items", []):
            vid = item["variant_id"]
            qty = item["quantity"]

            if vid not in variants:
                return jsonify({"error": "Variant not found"}), 404

            if variants[vid]["stock"] < qty:
                return jsonify({"error": "Insufficient stock"}), 400

            variants[vid]["stock"] -= qty

        return jsonify({"message": "Stock decreased"}), 200

    # -----------------------------
    # Login (for JWT testing)
    # -----------------------------
    @app.post("/login")
    def login():
        token = create_access_token(identity="1")
        return jsonify({"access_token": token}), 200

    app.register_blueprint(bp, url_prefix="/api/v1/products")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)