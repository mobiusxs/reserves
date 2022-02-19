from flask import Blueprint, render_template

from core.config import TEMPLATES_PATH
from . import database

bp = Blueprint('items', __name__, template_folder=TEMPLATES_PATH, url_prefix='/items')


@bp.route('/')
def index():
    items = database.list_items()
    return render_template('items/index.html', items=items)


@bp.route('/buy_all')
def buy_all():
    items = database.buy_all()
    return render_template('items/buy_all.html', items=items)
