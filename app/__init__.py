""" Entry point for run server application """
import os
from flask import Flask
from flask_migrate import Migrate


def create_app(test_config=None):
    # Initialize and setup Flask app
    app = Flask(__name__, instance_relative_config=True)
    db_uri = os.getenv("DATABASE_URI", os.path.join(app.instance_path, "app_db.sqlite"))
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "secret_key_123"),
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Db initialization
    from .models import db

    db.init_app(app)
    # Set migrations manager
    Migrate(app, db)

    # Schemas initialization
    from .schema import ma

    ma.init_app(app)

    # Views initialization
    from app.customer import customer

    app.register_blueprint(customer, url_prefix="/customer")

    # Celery app configuration
    app.config.update(
        CELERY_BROKER_URL=os.getenv("REDIS_URI"),
        CELERY_RESULT_URL=os.getenv("REDIS_URI"),
        CELERY_IMPORTS=("app.tasks.location",),
    )

    @app.route("/alive")
    def app_status():
        return {"status": "Server alive"}

    return app
