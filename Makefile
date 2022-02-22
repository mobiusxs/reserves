env:
	export FLASK_APP=core/app
	export FLASK_ENV=production
	export PYTHONPATH=${PYTHONPATH}:$(pwd)

db:
	python ./data/tables.py
	python ./data/static.py
	python ./data/orders.py
	python ./data/doctrines.py

run:
	gunicorn -w 4 -b 0.0.0.0:5000 "core.app:create_app()"
