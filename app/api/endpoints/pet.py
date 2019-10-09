# codign: utf-8

import uuid
from datetime import datetime
from flask import request, current_app, g
from flask_restplus import Namespace, Resource, abort
from pynamodb.exceptions import DoesNotExist
from ..security import auth
from ..serializers.pet import pet_model, pet_resource, pet_paginated_model
from ..parsers import pet_parser
from ...models import Pet, Position, PetLocation, Zone


ns = Namespace('pet', description='Pet related operations.')


@ns.route('')
class PetResource(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(pet_paginated_model)
    @ns.expect(pet_parser)
    def get(self):
        """
        Get pet list
        """
        args = pet_parser.parse_args()
        limit = args['limit'] if args['limit'] is not None else current_app.config['PER_PAGE']
        if limit <= 0:
            limit = current_app.config['PER_PAGE']
        
        key = None
        if args['key'] is not None:
            key = {
                'owner': {'S': g.user['username']},
                'name': {'S': args['key']}
            }
        
        try:
            iterator = Pet.query(g.user['username'], scan_index_forward=False, consistent_read=True, last_evaluated_key=key, limit=limit)
            result = {
                'pets': [pet for pet in iterator],
                'pagination': {
                    'current': args['key'],
                    'limit': limit,
                    'next': None
                }
            }
            last_key = iterator.last_evaluated_key
            if last_key is not None and last_key['name']['S'] != args['key'] and len(result['pets']) > 0:
                last_item = result['pets'][len(result['pets']) - 1]
                if str(last_item.name) == last_key['name']['S']:
                    result['pagination']['next'] = last_key['name']['S']
                    
            return result

        except Exception as ex:
            current_app.logger.error('Unable to get pets list : {0}'.format(ex))
            abort(400, 'Unable to get pets list, please try again later')

    @ns.expect(pet_model)
    @ns.marshal_with(pet_resource)
    def post(self):
        """
        Create pet
        """
        payload = request.json
        fake_start_position = Position(lat=50.635221, lng=3.058015)
        pet = Pet(
            id=str(uuid.uuid1()),
            owner=g.user['username'],
            name=payload['name'],
            serial=payload['serial'],
            picture=payload['picture'],
            description=payload['description'],
            location=PetLocation(
                at=datetime.timestamp(datetime.now()),
                position=fake_start_position
            ),
            zone=Zone(
                position=fake_start_position,
                radius=0.000600
            )
        )

        try:
            pet.save()

            return pet
        
        except Exception as ex:
            current_app.logger.error('Unable to create pet : {0}'.format(ex))
            abort(400, 'Unable to create pet, please try again later')