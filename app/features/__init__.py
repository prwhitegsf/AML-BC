from flask import Blueprint

bp = Blueprint('features', __name__)

from app.features import routes