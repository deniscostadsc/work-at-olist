#!/bin/bash

set -v

sudo apt update

sudo apt install -y \
    postgresql \
    python-pip

sudo apt autoremove
sudo apt autoclean

sudo -u postgres psql << EOC
    CREATE USER olist WITH PASSWORD 'olist';
    CREATE DATABASE olist;
    GRANT ALL PRIVILEGES ON DATABASE "olist" to olist;
    ALTER USER olist CREATEDB;
EOC

sudo -H pip install -U pip
sudo -H pip install virtualenv

virtualenv --python=python3 ~/olist-venv
source ~/olist-venv/bin/activate

pip install -r /vagrant/requirements-local.txt

echo 'cd /vagrant' >> ~/.bashrc
echo '. ~/olist-venv/bin/activate' >> ~/.bashrc
