from datetime import timedelta
from flask import Flask
import os
from src.auth import auth
from src.trending import trending
from src.database import db
from flask_jwt_extended import JWTManager
from src.favourites import favourites
from src.likes import likes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCKEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            MEDIA_FOLDER = os.environ.get("MEDIA_FOLDER"),
        )
    else:
        app.config.from_mapping(test_config)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=90)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(favourites)
    app.register_blueprint(trending)
    app.register_blueprint(likes)

    return app
