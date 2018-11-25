from config import Config
from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from sqlalchemy_searchable import make_searchable
from sqlalchemy.orm import configure_mappers

db = SQLAlchemy()

ma = Marshmallow()
jwt = JWTManager()

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Flask Searchable Requirnments
    make_searchable(db.metadata)
    configure_mappers()

    # Register blueprints from modules here!
    app.register_blueprint(api_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.datasets import bp as datasets_bp
    app.register_blueprint(datasets_bp)

    return app
