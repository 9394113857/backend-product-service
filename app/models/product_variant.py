from datetime import datetime
from app.extensions import db


class ProductVariant(db.Model):
    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    sku = db.Column(
        db.String(100),
        unique=True
    )

    color = db.Column(db.String(50))

    size = db.Column(db.String(50))

    stock = db.Column(
        db.Integer,
        default=0
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    image = db.Column(db.String(500))

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Variant "
            f"product={self.product_id} "
            f"sku={self.sku} "
            f"stock={self.stock}>"
        )