from flask import Blueprint

bp = Blueprint('server_main', __name__)

from app.server_main import routes