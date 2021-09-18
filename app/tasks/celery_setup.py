""" Celery setup """

from celery import Celery
from app import create_app


def make_celery(app=None):
    # Creates app if not exists
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_URL"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
