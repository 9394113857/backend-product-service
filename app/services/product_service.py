from ..models.product import Product
from ..extensions import db

def create_product(data):
    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"]
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_all_products():
    return Product.query.all()

def get_product(product_id):
    return Product.query.get(product_id)

def update_product(product_id, data):
    product = Product.query.get(product_id)
    if not product:
        return None

    if "name" in data:
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        product.price = data["price"]

    db.session.commit()
    return product

def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return None

    db.session.delete(product)
    db.session.commit()
    return True
