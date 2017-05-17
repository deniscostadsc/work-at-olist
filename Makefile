.DEFAULT: build

test:
	python3 work-at-olist/manage.py test

lint:
	flake8 .

build: lint test
