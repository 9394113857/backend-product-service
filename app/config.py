import os

class Config:
    # This key is used for session signing (not important for JWT)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # SQLite product DB
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///product.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # IMPORTANT: Must match auth-service JWT secret
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
