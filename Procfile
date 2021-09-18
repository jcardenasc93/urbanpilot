release: python -m flask db upgrade
web: gunicorn -w 4 wsgi:app
worker: python -m celery -A celery_worker worker --loglevel=info
