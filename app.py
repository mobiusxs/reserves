from flask import Flask, render_template, request
from dotenv import load_dotenv

from parsers import parse_eft
from market import get_availability
from eve_types import get_name_dict

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
    availability = get_availability(1035466617946)
    types = get_name_dict()
    fits_available = []
    for item_name, required in fitting['items'].items():
        type_id = types.get(item_name)
        available = availability.get(type_id, 0)
        data['items'][item_name] = {'required': required, 'available': available}
        fits_available.append(available // required)
    data['fits_available'] = min(fits_available)
    return data
