""" Entrypoint for gunicorn app deployment """
from app import create_app
from app.tasks.celery_setup import make_celery

app = create_app()
celery = make_celery(app)
app.celery = celery

if __name__ == "__main__":
    app.run(port=8008, debug=True)
