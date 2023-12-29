#!/bin/sh
python -m venv .venv
. .venv/bin/activate # run this again to activate venv
python -m pip install Django~=4.2
python manage.py makemigrations
python manage.py migrate