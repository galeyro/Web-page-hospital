#!/bin/bash
set -o errexit

pip install -r requirements.txt

cd hospital
python manage.py collectstatic --no-input
python manage.py migrate
