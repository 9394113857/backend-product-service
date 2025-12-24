from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.product import Product

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)

# ============================================================
# PRODUCT SERVICE HEALTH CHECK (AUTH-STYLE)
# GET /api/v1/products/
# ============================================================
@product_bp.get("/")
def product_service_health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# HEALTH CHECK (Angular expects this)
# GET /api/angularProduct/health
# ============================================================
@angular_product_bp.get("/health")
def angular_health():
    return jsonify({"status": "angular-product-service UP"}), 200


# ============================================================
# ANGULAR: ADD PRODUCT
# POST /api/angularProduct/add
# ============================================================
@angular_product_bp.post("/add")
@jwt_required()
def angular_add_product():
    data = request.get_json() or {}
    seller_id = get_jwt_identity()

    if "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400

    product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", "")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "_id": product.id,
        "name": product.name,
        "price": product.price
    }), 201


# ============================================================
# ANGULAR: GET ALL PRODUCTS
# GET /api/angularProduct/get
# ============================================================
@angular_product_bp.get("/get")
def angular_get_products():
    products = Product.query.all()

    return jsonify([
        {
            "_id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description
        }
        for p in products
    ]), 200


# ============================================================
# ANGULAR: GET SINGLE PRODUCT
# GET /api/angularProduct/get/<id>
# ============================================================
@angular_product_bp.get("/get/<int:id>")
def angular_get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "_id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description
    }), 200


# ============================================================
# ANGULAR: UPDATE PRODUCT
# PATCH /api/angularProduct/update
# ============================================================
@angular_product_bp.patch("/update")
@jwt_required()
def angular_update_product():
    data = request.get_json() or {}

    product_id = data.get("productId")
    updated_data = data.get("updatedData", {})

    if not product_id:
        return jsonify({"error": "productId required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    product.name = updated_data.get("name", product.name)
    product.price = updated_data.get("price", product.price)
    product.description = updated_data.get("description", product.description)

    db.session.commit()

    return jsonify({
        "message": "Product updated",
        "_id": product.id
    }), 200


# ============================================================
# ANGULAR: DELETE PRODUCT
# DELETE /api/angularProduct/delete
# ============================================================
@angular_product_bp.delete("/delete")
@jwt_required()
def angular_delete_product():
    data = request.get_json() or {}
    product_id = data.get("productId")

    if not product_id:
        return jsonify({"error": "productId required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200
