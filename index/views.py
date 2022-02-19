from flask import Blueprint, render_template, request

from core import config

bp = Blueprint('index', __name__, template_folder=config.TEMPLATES_PATH)


@bp.route('/')
def index():
    return render_template('index/index.html')
