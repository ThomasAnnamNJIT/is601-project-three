"""A simple flask web app"""
import os

import flask_login
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.admin import admin
from app.auth import auth
from app.cli import create_database
from app.db import db
from app.db import database
from flask_cors import CORS

from app.db.models import User
from app.error_handlers import error_handlers
from app.logging_config import log_con
from app.user import users

login_manager = flask_login.LoginManager()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    # https://flask-login.readthedocs.io/en/latest/  <-login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    # Needed for CSRF protection of form submissions and WTF Forms
    # https://wtforms.readthedocs.io/en/3.0.x/
    csrf = CSRFProtect(app)
    app.register_blueprint(database)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(users)
    # these load functionality without a web interface
    app.register_blueprint(log_con)
    app.register_blueprint(error_handlers)
    # add command function to cli commands
    app.cli.add_command(create_database)
    db.init_app(app)
    api_v1_cors_config = {
        "methods": ["OPTIONS", "GET", "POST"],
    }
    CORS(app, resources={"/api/*": api_v1_cors_config})
    # Run once at startup:
    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(str(e))
        return None
