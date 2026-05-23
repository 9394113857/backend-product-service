from datetime import datetime
from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    seller_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    category_id = db.Column(
        db.Integer,
        nullable=True
    )

    brand_id = db.Column(
        db.Integer,
        nullable=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    slug = db.Column(
        db.String(255),
        unique=True
    )

    description = db.Column(db.Text)

    base_price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    thumbnail_image = db.Column(
        db.String(500)
    )

    # ⚠ TEMP Angular compatibility
    color = db.Column(db.String(50))

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    variants = db.relationship(
        "ProductVariant",
        backref="product",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Product {self.id} {self.name}>"