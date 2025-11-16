release: python hospital/manage.py migrate
web: gunicorn hospital.wsgi:application --log-file -
