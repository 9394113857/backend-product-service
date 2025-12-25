from ..extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    # -------------------------------
    # PRIMARY KEY
    # -------------------------------
    id = db.Column(db.Integer, primary_key=True)

    # -------------------------------
    # CORE PRODUCT FIELDS
    # -------------------------------
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)

    # -------------------------------
    # ANGULAR FRONTEND FIELDS
    # (required to avoid 422 error)
    # -------------------------------
    image = db.Column(db.String(500))        # product image URL
    category = db.Column(db.String(100))     # Electronics, Fashion, etc.
    color = db.Column(db.String(50))          # Black, Red, etc.

    # -------------------------------
    # META
    # -------------------------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -------------------------------
    # DEBUG / LOGGING
    # -------------------------------
    def __repr__(self):
        return f"<Product {self.id} - {self.name}>"
