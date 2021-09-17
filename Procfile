release: python -m flask db upgrade
web: gunicorn -w 4 wsgi:app
