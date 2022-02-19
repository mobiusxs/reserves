from flask import Blueprint, redirect, render_template, request, url_for

from utils.parsers import parse_eft
from data.select import get_by_name

from core import config
from . import database

bp = Blueprint('fits', __name__, template_folder=config.TEMPLATES_PATH, url_prefix='/fits')


@bp.route('/')
def index():
    fits = database.list_fits()
    return render_template('fits/index.html', fits=fits)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fit_raw = request.form.get('fit')
        quantity = request.form.get('quantity')
        fit = parse_eft(fit_raw)
        fit_id = database.create_fit(fit, quantity)
        return redirect(url_for('fits.view', fit_id=fit_id))
    return render_template('fits/add.html')


@bp.route('/view/<int:fit_id>')
def view(fit_id):
    fit = database.read_fit(fit_id)
    return render_template('fits/view.html', fit=fit)
