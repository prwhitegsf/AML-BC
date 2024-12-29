import pytest

import flask
from sqlalchemy import text
from app import db
from app import create_app

from config import TestConfig
#from flask import session as sess
import random, string

def generate_random_name(len=5):
     letters = string.ascii_lowercase
     name = ''.join(random.choice(letters) for i in range(len))
     return name


@pytest.fixture(scope='session')
def app():


    app = create_app(config_class=TestConfig)
    
    
    yield app
    
       
@pytest.fixture(scope='session')
def app_ctx(app):
    with app.app_context():
        yield
       # app.session_interface.client.session.execute(text("DELETE FROM sessions"))
       # app.session_interface.client.session.close()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()