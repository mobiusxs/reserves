from flask import Flask

from index.views import bp as bp_index
from fits.views import bp as bp_fit
from items.views import bp as bp_items


def create_app():
    app = Flask(__name__)
    app = register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_fit)
    app.register_blueprint(bp_items)
    return app
