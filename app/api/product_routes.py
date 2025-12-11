from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.product import Product

product_bp = Blueprint("products", __name__)

# ============================================================
# Helper: return JSON 404 instead of HTML 404
# ============================================================
def product_not_found(id):
    return jsonify({"error": f"Product with id {id} not found"}), 404


# ============================================================
# CREATE PRODUCT
# ============================================================
@product_bp.post("/")
@jwt_required()
def create_product():
    data = request.get_json() or {}

    # Validation
    if "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400

    p = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", "")
    )

    db.session.add(p)
    db.session.commit()

    return jsonify({"message": "Product created", "product_id": p.id}), 201


# ============================================================
# GET ALL PRODUCTS
# ============================================================
@product_bp.get("/")
@jwt_required()
def get_products():
    products = Product.query.all()

    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price, "description": p.description}
        for p in products
    ]), 200


# ============================================================
# GET PRODUCT BY ID (Graceful error handling)
# ============================================================
@product_bp.get("/<int:id>")
@jwt_required()
def get_product(id):
    p = Product.query.get(id)

    if not p:
        return product_not_found(id)

    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description
    }), 200


# ============================================================
# UPDATE PRODUCT (Graceful error handling)
# ============================================================
@product_bp.put("/<int:id>")
@jwt_required()
def update_product(id):
    data = request.get_json() or {}
    p = Product.query.get(id)

    if not p:
        return product_not_found(id)

    p.name = data.get("name", p.name)
    p.price = data.get("price", p.price)
    p.description = data.get("description", p.description)

    db.session.commit()

    return jsonify({"message": "Product updated", "product_id": p.id}), 200


# ============================================================
# DELETE PRODUCT (Graceful error handling)
# ============================================================
@product_bp.delete("/<int:id>")
@jwt_required()
def delete_product(id):
    p = Product.query.get(id)

    if not p:
        return product_not_found(id)

    db.session.delete(p)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200
