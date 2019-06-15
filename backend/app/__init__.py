from config import Config
from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.lib.errors import errors
from flask_mail import Mail
from elasticsearch import Elasticsearch


db = SQLAlchemy()

ma = Marshmallow()
jwt = JWTManager()
mail = Mail()
cors = CORS()

api_bp = Blueprint('api', __name__)
api = Api(api_bp, errors=errors)


def create_app(config_class=Config):
    app = Flask(__name__)

    # TODO: If production only accept requests from frontend host
    # See: https://flask-cors.readthedocs.io/en/latest/api.html
    cors.init_app(app, resources={r'*': {
            'origins': '*',
            'supports_credentials': True
        }
    })

    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.auth.blacklist_helpers import is_token_revoked
    # Checks if token is revoked before allowing access to a protected endpoint
    @jwt.token_in_blacklist_loader
    def check_if_token_revoked(decoded_token):
        return is_token_revoked(decoded_token)

    # Register blueprints from modules here!
    app.register_blueprint(api_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.datasets import bp as datasets_bp
    app.register_blueprint(datasets_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
