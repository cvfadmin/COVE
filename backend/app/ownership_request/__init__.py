from flask import Blueprint

bp = Blueprint('ownership_request', __name__)

from app.ownership_request import routes