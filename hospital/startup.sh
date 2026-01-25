#!/bin/bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --no-input

echo "Seeding demo data..."
python seed_demo_data.py

echo "Starting Gunicorn..."
exec gunicorn hospital.wsgi:application --log-file -
