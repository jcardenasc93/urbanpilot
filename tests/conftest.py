""" Test cases for the app """

import os
import pytest
from alembic.command import upgrade
from alembic.config import Config
from app.models import db as _db
from app import create_app

TEST_DB = "app_test.db"
TEST_DB_PATH = f"instance/{TEST_DB}"
TEST_DB_URI = f"sqlite:///{TEST_DB_PATH}"


def apply_alembic_migrations():
    ALEMBIC_CONFIG = "migrations/alembic.ini"
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, "head")


@pytest.fixture(scope="session")
def app(request):
    """Defines Flask app for testing"""
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": TEST_DB_URI})

    # Set app context
    app_context = app.app_context()
    app_context.push()

    def teardown():
        app_context.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    """Handles creating and dropping db for each test session"""
    if os.path.exists(TEST_DB_PATH):
        # Clear any previous db links
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        if os.path.exists(TEST_DB_PATH):
            os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """Creates new db session per test"""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="session")
def celery_app():
    """Setup celery app for testing"""
    from run import celery
    from celery.contrib.testing import tasks

    return celery
