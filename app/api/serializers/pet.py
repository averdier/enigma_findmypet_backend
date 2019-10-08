# coding: utf-8

from datetime import datetime
from flask_restplus import fields
from .import pagination_model, position_model, api


pet_location = api.model('Pet location', {
    'at': fields.DateTime(required=True, description='Pet creation datetime', attribute=lambda x: datetime.fromtimestamp(x.at).isoformat()),
    'position': fields.Nested(position_model, required=True)
})

pet_model = api.model('Pet', {
    'name': fields.String(required=True, min_length=3, max_length=32, description='Pet name'),
    'serial': fields.String(required=True, min_length=12, max_length=32, description='Pet serial'),
    'picture': fields.String(required=True, description='Pet picture'),
    'description': fields.String(required=True, max_length=512, description='Pet description')
})

pet_resource = api.inherit('Pet resource', pet_model, {
    'id': fields.String(required=True, description='Pet unique ID'),
    'created_at': fields.DateTime(required=True, description='Pet creation datetime', attribute=lambda x: datetime.fromtimestamp(x.created_at).isoformat()),
    'location': fields.Nested(pet_location, required=True, description='Pet location')
})

pet_paginated_model = api.model('Pet paginated', {
    'pets': fields.List(fields.Nested(pet_resource), required=True, description='Pets list'),
    'pagination': fields.Nested(pagination_model, required=True, description='Pagination')
})