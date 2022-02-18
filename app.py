from flask import Flask, render_template, request
from dotenv import load_dotenv

from utils.parsers import parse_eft
from data.select import get_by_name

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        fit = request.form.get('fit')
        data = get_fit_availability(fit)
        return render_template('result.html', name=data['name'], fits_available=data['fits_available'], items=data['items'])
    return render_template('check.html')


def get_fit_availability(fit):
    fitting = parse_eft(fit)
    data = {'name': fitting['name'], 'items': {}}

    fits_available = []
    for item_name, required in fitting['items'].items():
        type_id, name, volume, price = get_by_name(item_name)
        data['items'][item_name] = {'required': required, 'available': volume}
        fits_available.append(volume // required)
    data['fits_available'] = min(fits_available)
    return data
