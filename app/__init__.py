import os
from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors, setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logging
    setup_logging(app)

    app.logger.info("Product service initializing...")

    # Initialize extensions
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprint
    from .api.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/v1/products")

    app.logger.info("Product service started and routes registered.")
    return app
