import logging
from logging.handlers import RotatingFileHandler

import os
from flask import Flask, session
from flask_session import Session

from config import Config
from app.models import db

sess = Session()
Config.SESSION_SQLALCHEMY = db


def create_app(config_class=Config):
    
    # App object from config class
    app = Flask(__name__)
    app.config_from_object(config_class)

    # Register blueprints
    from app.intro import bp as intro_bp
    app.register_blueprint(intro_bp)

    from app.features import bp as feature_bp
    app.register_blueprint(feature_bp) 
    
    from app.labels import bp as labels_bp
    app.register_blueprint(labels_bp)


    # logging, useful when deployed to production
    if not app.debug and not app.testing:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/test.log',
                                        maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('test startup')


    return app