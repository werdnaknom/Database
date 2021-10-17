from flask import Blueprint

bp = Blueprint('api_upload', __name__)

from app.api_upload import routes