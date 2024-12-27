import logging
from logging.handlers import RotatingFileHandler

import os
from flask import Flask, session
#from flask_session import Session

from config import Config
from app.main.models import db

#sess = Session()
#Config.SESSION_SQLALCHEMY = db


def create_app(config_class=Config):
    
    # App object from config class
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # Register blueprints
   
    from app.main import bp as main_bp
    app.register_blueprint(main_bp) 
    



   
    
    #sess.init_app(app)

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