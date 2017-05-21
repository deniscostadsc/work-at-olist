.DEFAULT: build

build: lint test

test:
	cd work-at-olist; coverage run --source='.' manage.py test

lint:
	flake8 .

migrate:
	cd work-at-olist; python3 manage.py migrate

makemigrations:
	cd work-at-olist; python3 manage.py makemigrations

coverage:
	cd work-at-olist; coverage report -m
