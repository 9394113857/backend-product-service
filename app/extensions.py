from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from logging.handlers import TimedRotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def setup_logging(app):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    handler = TimedRotatingFileHandler(
        "logs/product.log",
        when="midnight",
        backupCount=7,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
