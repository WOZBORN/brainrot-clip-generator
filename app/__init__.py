from flask import Flask
from .routes import bp as scheduler_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    app.register_blueprint(scheduler_bp, url_prefix="")

    return app
