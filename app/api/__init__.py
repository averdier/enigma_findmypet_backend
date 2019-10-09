# coding: utf-8

import os
from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    title='FindMyPet Backend',
    description='Swagger documentation of FindMyPet backend (only for local purpose)',
    doc='/' if os.environ.get('APP_CONFIG') == 'dev' else None,
    authorizations={
        'tokenKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    security='tokenKey'
)

from .endpoints.pet import ns as pet_namespace
from .endpoints.subscription import ns as subscription_namespace

api.add_namespace(pet_namespace)
api.add_namespace(subscription_namespace)