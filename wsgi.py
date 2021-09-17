""" Entrypoint for gunicorn app deployment """
from app import create_app

app = create_app()
