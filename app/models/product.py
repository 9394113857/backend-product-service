# ============================================================
# FILE: app/models/product.py
# PURPOSE: Product model for Angular + Flask microservice
# DATABASE: PostgreSQL (Neon)
# ORM: Flask-SQLAlchemy
# ============================================================

from datetime import datetime
from ..extensions import db


class Product(db.Model):
    """
    Product table definition.

    IMPORTANT:
    - This model MUST match the PostgreSQL schema exactly.
    - Missing columns will cause 500 errors (as seen with 'image').
    """

    __tablename__ = "products"

    # --------------------------------------------------------
    # PRIMARY KEY
    # --------------------------------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # --------------------------------------------------------
    # CORE PRODUCT FIELDS (BUSINESS DATA)
    # --------------------------------------------------------
    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.String(500),
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    # --------------------------------------------------------
    # ANGULAR FRONTEND FIELDS
    # These fields are REQUIRED because Angular sends/expects them
    # Missing DB columns here will cause SQLAlchemy 500 errors
    # --------------------------------------------------------
    image = db.Column(
        db.String(500),
        nullable=True
    )  # Product image URL

    category = db.Column(
        db.String(100),
        nullable=True
    )  # Electronics, Fashion, etc.

    color = db.Column(
        db.String(50),
        nullable=True
    )  # Black, Red, etc.

    # --------------------------------------------------------
    # META / AUDIT FIELDS
    # --------------------------------------------------------
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # --------------------------------------------------------
    # DEBUG / LOGGING REPRESENTATION
    # --------------------------------------------------------
    def __repr__(self):
        return f"<Product id={self.id}, name='{self.name}'>"
