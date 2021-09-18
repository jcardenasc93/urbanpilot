from celery import Celery
import os


def make_celery():
    celery = Celery(
        "app",
        backend=os.getenv("REDIS_URI"),
        broker=os.getenv("REDIS_URI"),
        include=["app.tasks.location"],
    )

    return celery


celery = make_celery()
