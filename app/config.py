import os
from dotenv import load_dotenv

# 🔹 Load .env if present (safe – ignored in Render)
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "product-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///product.db"   # ✅ fallback (unchanged)
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key"
    )
