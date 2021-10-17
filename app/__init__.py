from flask import Flask
from config import Config
from flask_wtf import CSRFProtect

from flask_bootstrap import Bootstrap

def create_app(config_class=Config):
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    CSRFProtect(app)
    app.config.from_object(config_class)

    from app.api_upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix="/api_upload")

    return app

