.DEFAULT: build

build: lint test coverage

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

create-vm:
	vagrant  up
	vagrant snapshot save right-after-provision

destroy-vm:
	vagrant destroy -f

recreate-vm: destroy-vm create-vm

reset-vm:
	vagrant snapshot restore right-after-provision
