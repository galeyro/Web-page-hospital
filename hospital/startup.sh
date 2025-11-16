#!/bin/bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --no-input

echo "Creating admin user..."
python create_admin.py

echo "Starting Gunicorn..."
exec gunicorn hospital.wsgi:application --log-file -
