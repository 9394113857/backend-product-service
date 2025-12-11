from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.product import Product

product_bp = Blueprint("products", __name__)

# ============================================================
# HEALTH CHECK
# ============================================================
@product_bp.get("/")
def health_check():
    current_app.logger.info("[PRODUCT-SERVICE] Health check OK")
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# Helper: return JSON 404 instead of HTML 404
# ============================================================
def product_not_found(id):
    current_app.logger.warning(f"[PRODUCT] NOT FOUND id={id}")
    return jsonify({"error": f"Product with id {id} not found"}), 404


# ============================================================
# CREATE PRODUCT
# ============================================================
@product_bp.post("/")
@jwt_required()
def create_product():
    data = request.get_json() or {}

    current_app.logger.info(f"[PRODUCT CREATE] Payload={data}")

    # Validation
    if "name" not in data or "price" not in data:
        current_app.logger.warning("[PRODUCT CREATE] Missing required fields")
        return jsonify({"error": "name and price are required"}), 400

    p = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", "")
    )

    db.session.add(p)
    db.session.commit()

    current_app.logger.info(f"[PRODUCT CREATE] SUCCESS product_id={p.id}")

    return jsonify({"message": "Product created", "product_id": p.id}), 201


# ============================================================
# GET ALL PRODUCTS
# ============================================================
@product_bp.get("/all")
@jwt_required()
def get_products():
    current_app.logger.info("[PRODUCT LIST] Fetching all products")

    products = Product.query.all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description
        }
        for p in products
    ]

    current_app.logger.info(f"[PRODUCT LIST] Count={len(result)}")

    return jsonify(result), 200


# ============================================================
# GET PRODUCT BY ID (Graceful error handling)
# ============================================================
@product_bp.get("/<int:id>")
@jwt_required()
def get_product(id):
    current_app.logger.info(f"[PRODUCT FETCH] id={id}")

    p = Product.query.get(id)
    if not p:
        return product_not_found(id)

    current_app.logger.info(f"[PRODUCT FETCH] FOUND id={id}")

    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description
    }), 200


# ============================================================
# UPDATE PRODUCT
# ============================================================
@product_bp.put("/<int:id>")
@jwt_required()
def update_product(id):
    data = request.get_json() or {}
    current_app.logger.info(f"[PRODUCT UPDATE] id={id} payload={data}")

    p = Product.query.get(id)
    if not p:
        return product_not_found(id)

    p.name = data.get("name", p.name)
    p.price = data.get("price", p.price)
    p.description = data.get("description", p.description)

    db.session.commit()

    current_app.logger.info(f"[PRODUCT UPDATE] SUCCESS id={p.id}")

    return jsonify({"message": "Product updated", "product_id": p.id}), 200


# ============================================================
# DELETE PRODUCT
# ============================================================
@product_bp.delete("/<int:id>")
@jwt_required()
def delete_product(id):
    current_app.logger.info(f"[PRODUCT DELETE] Attempt id={id}")

    p = Product.query.get(id)
    if not p:
        return product_not_found(id)

    db.session.delete(p)
    db.session.commit()

    current_app.logger.info(f"[PRODUCT DELETE] SUCCESS id={id}")

    return jsonify({"message": "Product deleted"}), 200
