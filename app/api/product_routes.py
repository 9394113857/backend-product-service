from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.models.product import Product
from app.models.product_variant import ProductVariant

from app.services.product_service import (
    create_product,
    get_product,
    get_all_products,
    create_variant
)

from app.extensions import db


product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)


# ============================================================
# HEALTH
# ============================================================
@product_bp.get("/")
def health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# ADD PRODUCT
# ============================================================
@product_bp.post("/add")
@jwt_required()
def add_product():

    data = request.get_json()

    product = create_product(data)

    return jsonify({
        "id": product.id,
        "name": product.name,
        "base_price": str(product.base_price),
        "message": "Product created successfully"
    }), 201


# ============================================================
# GET ALL PRODUCTS
# ============================================================
@product_bp.get("/list")
def list_products():

    products = get_all_products()

    return jsonify([
        {
            "id": p.id,
            "seller_id": p.seller_id,
            "name": p.name,
            "slug": p.slug,
            "description": p.description,
            "base_price": str(p.base_price),
            "thumbnail_image": p.thumbnail_image,

            # ⚠ Angular compatibility
            "color": p.color,

            "variants": [
                {
                    "variant_id": v.id,
                    "sku": v.sku,
                    "color": v.color,
                    "size": v.size,
                    "stock": v.stock,
                    "price": str(v.price),
                    "image": v.image
                }
                for v in p.variants
                if v.is_active
            ]
        }
        for p in products
    ]), 200


# ============================================================
# GET SINGLE PRODUCT
# ============================================================
@product_bp.get("/<int:product_id>")
def get_single_product(product_id):

    p = get_product(product_id)

    if not p:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": p.id,
        "seller_id": p.seller_id,
        "name": p.name,
        "slug": p.slug,
        "description": p.description,
        "base_price": str(p.base_price),
        "thumbnail_image": p.thumbnail_image,

        # ⚠ Angular compatibility
        "color": p.color,

        "variants": [
            {
                "variant_id": v.id,
                "sku": v.sku,
                "color": v.color,
                "size": v.size,
                "stock": v.stock,
                "price": str(v.price),
                "image": v.image
            }
            for v in p.variants
            if v.is_active
        ]
    }), 200


# ============================================================
# ADD VARIANT
# ============================================================
@product_bp.post("/<int:product_id>/variants")
@jwt_required()
def add_product_variant(product_id):

    Product.query.get_or_404(product_id)

    data = request.get_json()

    variant = create_variant(product_id, data)

    return jsonify({
        "variant_id": variant.id,
        "sku": variant.sku,
        "message": "Variant added successfully"
    }), 201


# ============================================================
# DECREASE STOCK
# ============================================================
@product_bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():

    data = request.get_json() or {}
    items = data.get("items", [])

    for item in items:

        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"],
            is_active=True
        ).first()

        if not variant:
            return jsonify({
                "error": "Variant not found"
            }), 404

        if variant.stock < item["quantity"]:
            return jsonify({
                "error": "Insufficient stock",
                "variant_id": variant.id,
                "available": variant.stock
            }), 400

        variant.stock -= item["quantity"]

    db.session.commit()

    return jsonify({
        "message": "Stock decreased successfully"
    }), 200


# ============================================================
# RESTORE STOCK
# ============================================================
@product_bp.post("/restore-stock")
@jwt_required()
def restore_stock():

    data = request.get_json() or {}
    items = data.get("items", [])

    for item in items:

        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"],
            is_active=True
        ).first()

        if not variant:
            return jsonify({
                "error": "Variant not found"
            }), 404

        variant.stock += item["quantity"]

    db.session.commit()

    return jsonify({
        "message": "Stock restored successfully"
    }), 200


# ============================================================
# ANGULAR COMPATIBILITY ROUTES
# ============================================================
@angular_product_bp.get("/get")
def angular_get_all():
    return list_products()


@angular_product_bp.get("/get/<int:product_id>")
def angular_get_single(product_id):
    return get_single_product(product_id)