from app.extensions import db

from app.models.product import Product
from app.models.product_variant import ProductVariant


# ============================================================
# CREATE PRODUCT
# ============================================================
def create_product(data):

    product = Product(

        # ====================================================
        # ✅ SAFE DEFAULT FOR OLD ANGULAR UI
        # ====================================================
        # Old Angular payload does not send seller_id
        # So temporarily default to seller_id = 1
        # ====================================================
        seller_id=data.get("seller_id", 1),

        # ====================================================
        # 🟩 OPTIONAL NEW FIELDS
        # ====================================================
        category_id=data.get("category_id"),

        brand_id=data.get("brand_id"),

        slug=data.get("slug"),

        # ====================================================
        # 🟦 REQUIRED FIELDS
        # ====================================================
        name=data["name"],

        description=data.get("description"),

        # ====================================================
        # 🔥 OLD + NEW PAYLOAD SUPPORT
        # ====================================================
        # Supports:
        # old Angular → price
        # new backend → base_price
        # ====================================================
        base_price=(
            data.get("base_price")
            or data.get("price")
        ),

        # ====================================================
        # 🔥 OLD + NEW IMAGE SUPPORT
        # ====================================================
        # Supports:
        # old Angular → image
        # new backend → thumbnail_image
        # ====================================================
        thumbnail_image=(
            data.get("thumbnail_image")
            or data.get("image")
        ),

        # ====================================================
        # ⚠ TEMP Angular Compatibility
        # ====================================================
        color=data.get("color")
    )

    db.session.add(product)
    db.session.commit()

    return product


# ============================================================
# GET SINGLE PRODUCT
# ============================================================
def get_product(product_id):

    return Product.query.filter_by(
        id=product_id,
        is_active=True
    ).first()


# ============================================================
# GET ALL PRODUCTS
# ============================================================
def get_all_products():

    return Product.query.filter_by(
        is_active=True
    ).all()


# ============================================================
# CREATE PRODUCT VARIANT
# ============================================================
def create_variant(product_id, data):

    variant = ProductVariant(

        product_id=product_id,

        # ====================================================
        # 🟩 NEW OPTIONAL FIELDS
        # ====================================================
        sku=data.get("sku"),

        size=data.get("size"),

        # ====================================================
        # 🟦 COMMON FIELDS
        # ====================================================
        color=data.get("color"),

        stock=data.get("stock", 0),

        # ====================================================
        # 🔥 OLD + NEW PRICE SUPPORT
        # ====================================================
        price=(
            data.get("price")
            or data.get("base_price")
            or 0
        ),

        # ====================================================
        # 🔥 OLD + NEW IMAGE SUPPORT
        # ====================================================
        image=(
            data.get("image")
            or data.get("thumbnail_image")
        )
    )

    db.session.add(variant)
    db.session.commit()

    return variant


# ============================================================
# DECREASE VARIANT STOCK
# ============================================================
def decrease_variant_stock(items):

    for item in items:

        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"],
            is_active=True
        ).first()

        if not variant:
            return {
                "success": False,
                "error": "Variant not found"
            }

        if variant.stock < item["quantity"]:
            return {
                "success": False,
                "error": "Insufficient stock",
                "variant_id": variant.id,
                "available": variant.stock
            }

        variant.stock -= item["quantity"]

    db.session.commit()

    return {
        "success": True,
        "message": "Stock decreased successfully"
    }


# ============================================================
# RESTORE VARIANT STOCK
# ============================================================
def restore_variant_stock(items):

    for item in items:

        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"],
            is_active=True
        ).first()

        if not variant:
            return {
                "success": False,
                "error": "Variant not found"
            }

        variant.stock += item["quantity"]

    db.session.commit()

    return {
        "success": True,
        "message": "Stock restored successfully"
    }