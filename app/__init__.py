from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object("config.Config")

    # Register routes
    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app
