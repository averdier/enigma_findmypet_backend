# coding: utf-8

from flask import Flask
from flask_cors import CORS
from config import config


def create_app(config_name='default'):

    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(config.get(config_name, config['default']))
    config.get(config_name, config['default']).init_app(app)

    from .api import blueprint as api_blueprint

    app.register_blueprint(api_blueprint)

    return app