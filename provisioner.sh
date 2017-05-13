#!/bin/bash

set -v

sudo apt update

sudo apt install -y \
    postgresql \
    python-pip

sudo apt autoremove
sudo apt autoclean

sudo -H pip install -U pip
sudo -H pip install -r /vagrant/requirements-local.txt

echo 'cd /vagrant' >> ~/.bashrc
