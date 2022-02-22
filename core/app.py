from flask import Flask

from core import config
from doctrine.views import bp as bp_doctrine


def create_app():
    app = Flask(__name__, static_folder=config.STATIC_FOLDER)
    app = register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(bp_doctrine)
    return app
