from celery import Celery
from app.tasks.celery_setup import make_celery

celery = make_celery()
