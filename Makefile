.DEFAULT: test

test:
	python3 work-at-olist/manage.py test

lint:
	flake8 .
