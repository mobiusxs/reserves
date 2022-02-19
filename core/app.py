from flask import Flask

from index.views import bp as bp_index
from doctrine.views import bp as bp_doctrine
from items.views import bp as bp_items


def create_app():
    app = Flask(__name__)
    app = register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_doctrine)
    app.register_blueprint(bp_items)
    return app
