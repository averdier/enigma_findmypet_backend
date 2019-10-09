# coding: utf-8

from flask_restplus import fields
from .. import api


class NullableInteger(fields.Integer):
    __schema_type__ = ['integer', 'null']
    __schema_example__ = 'nullable integer'


subscription_keys_model = api.model('Subscription keys', {
    'p256dh': fields.String(required=True, description='p256dh key'),
    'auth': fields.String(required=True, description='auth key')
})

subscription_endpoint_model = api.model('Subscription endpoint', {
    'endpoint': fields.String(required=True, description='Endpoint')
})

subscription_model = api.inherit('Subscription', subscription_endpoint_model, {
    'expiration_time': NullableInteger(required=True, description='Expiration time'),
    'keys': fields.Nested(subscription_keys_model, required=True, descriptions='Keys')
})

subscription_item_model = api.inherit('Subscription item', subscription_model, {
    'created_at': fields.DateTime(required=True, description='Creation datetime'),
})
