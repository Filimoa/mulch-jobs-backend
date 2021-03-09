from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import TestConfig, ProdConfig


db = SQLAlchemy()
migrate = Migrate()


def create_app(env="PROD"):
    if env == "TEST":
        config_class = TestConfig
    else:
        config_class = ProdConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


if __name__ == "__main__":
    create_app()
