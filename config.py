# coding: utf-8

import os
import secrets


class Config:

    SECRET_KEY = os.environ.get('APP_SECRET', secrets.token_urlsafe(16))
    NAME = os.environ.get('APP_NAME', 'findmypet')

    PROVIDER_REGION = os.environ.get('PROVIDER_REGION', 'eu-central-1')
    AUTH_POOL = os.environ.get('AUTH_POOL', '')
    AUTH_CLIENT_ID = os.environ.get('AUTH_CLIENT_ID', '')

    PER_PAGE = abs(int(os.environ.get('PER_PAGE', '35')))

    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True
    JSON_SORT_KEYS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    'dev': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}