from flask import Blueprint, redirect, render_template, request, url_for

from utils.parsers import parse_eft

from core import config
from . import database

bp = Blueprint('doctrine', __name__, template_folder=config.TEMPLATES_PATH)


@bp.route('/')
def index():
    doctrines = database.list_doctrines()
    return render_template('doctrine/index.html', doctrines=doctrines)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        eft_paste = request.form.get('eft')
        required = int(request.form.get('required'))
        eft_dict = parse_eft(eft_paste)
        id = database.create_doctrine(eft_dict, required)
        return redirect(url_for('doctrine.doctrine', id=id))
    return render_template('doctrine/add.html')


@bp.route('/doctrine/<int:id>')
def doctrine(id):
    doctrine_dict = database.get_doctrine(id)
    return render_template('doctrine/doctrine.html', doctrine=doctrine_dict)


@bp.route('/items')
def items():
    doctrine_items = database.get_doctrine_items()
    return render_template('doctrine/items.html', items=doctrine_items)


@bp.route('/missing')
def missing():
    missing_items = database.get_missing_items()
    return render_template('doctrine/missing.html', items=missing_items)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        eft_paste = request.form.get('eft')
        required = request.form.get('required', None)
        if eft_paste:
            eft_dict = parse_eft(eft_paste)
        else:
            eft_dict = None
        id = database.update_doctrine(id, eft_dict, required)
        return redirect(url_for('doctrine.doctrine', id=id))
    return render_template('doctrine/update.html', id=id)


@bp.route('/delete/<int:id>')
def delete(id):
    database.delete_doctrine(id)
    return redirect(url_for('doctrine.index'))
