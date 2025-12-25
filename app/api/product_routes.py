from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.product import Product

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)

# ============================================================
# PRODUCT SERVICE HEALTH CHECK
# GET /api/v1/products/
# ============================================================
@product_bp.get("/")
def product_service_health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# ANGULAR HEALTH CHECK
# GET /api/angularProduct/health
# ============================================================
@angular_product_bp.get("/health")
def angular_health():
    return jsonify({"status": "angular-product-service UP"}), 200


# ============================================================
# ANGULAR: ADD PRODUCT  ✅ FIXED
# POST /api/angularProduct/add
# ============================================================
@angular_product_bp.post("/add")
@jwt_required()
def angular_add_product():
    data = request.get_json() or {}
    seller_id = get_jwt_identity()  # future use (ownership)

    # ----------------------------
    # BASIC VALIDATION
    # ----------------------------
    name = data.get("name")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "name and price are required"}), 400

    # ----------------------------
    # SAFE PRICE CONVERSION
    # ----------------------------
    try:
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({"error": "price must be a number"}), 400

    # ----------------------------
    # CREATE PRODUCT (ALL FIELDS)
    # ----------------------------
    product = Product(
        name=name,
        price=price,
        description=data.get("description", ""),
        image=data.get("image", ""),
        category=data.get("category", ""),
        color=data.get("color", "")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "_id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image": product.image,
        "category": product.category,
        "color": product.color
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
            "description": p.description,
            "image": p.image,
            "category": p.category,
            "color": p.color
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
        "description": product.description,
        "image": product.image,
        "category": product.category,
        "color": product.color
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
    product.price = float(updated_data.get("price", product.price))
    product.description = updated_data.get("description", product.description)
    product.image = updated_data.get("image", product.image)
    product.category = updated_data.get("category", product.category)
    product.color = updated_data.get("color", product.color)

    db.session.commit()

    return jsonify({"message": "Product updated", "_id": product.id}), 200


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
