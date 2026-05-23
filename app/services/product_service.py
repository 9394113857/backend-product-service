from app.extensions import db
from app.models.product import Product
from app.models.product_variant import ProductVariant


def create_product(data):

    product = Product(
        seller_id=data["seller_id"],
        category_id=data.get("category_id"),
        brand_id=data.get("brand_id"),
        name=data["name"],
        slug=data.get("slug"),
        description=data.get("description"),
        base_price=data["base_price"],
        thumbnail_image=data.get("thumbnail_image"),
        color=data.get("color")
    )

    db.session.add(product)
    db.session.commit()

    return product


def get_product(product_id):

    return Product.query.filter_by(
        id=product_id,
        is_active=True
    ).first()


def get_all_products():

    return Product.query.filter_by(
        is_active=True
    ).all()


def create_variant(product_id, data):

    variant = ProductVariant(
        product_id=product_id,
        sku=data.get("sku"),
        color=data.get("color"),
        size=data.get("size"),
        stock=data.get("stock", 0),
        price=data["price"],
        image=data.get("image")
    )

    db.session.add(variant)
    db.session.commit()

    return variant