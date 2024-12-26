import pytest

import flask
from sqlalchemy import text
from app import db
from app import create_app

from config import TestConfig



@pytest.fixture(scope='session')
def app():

    TestConfig.SESSION_SQLALCHEMY = db
    app = create_app(config_class=TestConfig)

    yield app
    
       
@pytest.fixture(scope='session')
def app_ctx(app):
    with app.app_context():
        yield
        app.session_interface.client.session.execute(text("DELETE FROM sessions"))
        app.session_interface.client.session.close()


@pytest.fixture()
def client(app):
    return app.test_client()