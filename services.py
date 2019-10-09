# coding: utf-8

import os
import boto3
import json
from random import randint
from datetime import datetime
from pywebpush import webpush, WebPushException
from app.models import Pet, PetLocation, Position, PushSubscription


def is_in_zone(zone, position):
    return zone.position.lat - zone.radius < position['lat'] < zone.position.lat + zone.radius \
        and zone.position.lng - zone.radius < position['lng'] < zone.position.lng + zone.radius

def fake_update_pets_location (event, context):
    step = 0.000100
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=os.environ.get('PET_QUEUE'))

        pets = [pet for pet in Pet.scan()]
        for pet in pets:
            body = json.dumps({
                'owner': pet.owner,
                'name': pet.name,
                'at': datetime.timestamp(datetime.now()),
                'position': {
                    'lat': pet.location.position.lat - step if randint(0, 1) else pet.location.position.lat + step,
                    'lng': pet.location.position.lng - step if randint(0, 1) else pet.location.position.lng + step
                }
            })
            queue.send_message(
                MessageAttributes={
                    'Kind': {
                        'DataType': 'String',
                        'StringValue': 'location-update'
                    }
                },
                MessageBody=(body)
            )
            print('update location for : {0}'.format(pet.name))
    
    except Exception as ex:
        print(ex)


def fake_big_update_pets_location (event, context):
    step = 0.000700
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=os.environ.get('PET_QUEUE'))

        pets = [pet for pet in Pet.scan()]
        for pet in pets:
            body = json.dumps({
                'owner': pet.owner,
                'name': pet.name,
                'at': datetime.timestamp(datetime.now()),
                'position': {
                    'lat': pet.location.position.lat - step if randint(0, 1) else pet.location.position.lat + step,
                    'lng': pet.location.position.lng - step if randint(0, 1) else pet.location.position.lng + step
                }
            })
            queue.send_message(
                MessageAttributes={
                    'Kind': {
                        'DataType': 'String',
                        'StringValue': 'location-update'
                    }
                },
                MessageBody=(body)
            )
            print('update location for : {0}'.format(pet.name))
    
    except Exception as ex:
        print(ex)


def handle_pet_location_update (event, context):
    try:
        for record in event['Records']:
            payload = json.loads(record['body'])
            pets = Pet.query(payload['owner'], Pet.name == payload['name'])
            for pet in pets:
                pet.update(
                    actions=[
                        Pet.location.set(
                            PetLocation(
                                at=payload['at'],
                                position=Position(
                                    lat=payload['position']['lat'],
                                    lng=payload['position']['lng']
                                )
                            )
                        )
                    ]
                )
                print('save location for : {0}'.format(pet.name))
    
    except Exception as ex:
        print(ex)


def pet_zone_alert (event, context):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=os.environ.get('PUSH_QUEUE'))
        for record in event['Records']:
            payload = json.loads(record['body'])
            pets = Pet.query(payload['owner'], Pet.name == payload['name'])
            for pet in pets:
                if not is_in_zone(pet.zone, payload['position']):
                    body = json.dumps({
                        'owner': pet.owner,
                        'name': pet.name,
                    })
                    queue.send_message(
                        MessageAttributes={
                            'Kind': {
                                'DataType': 'String',
                                'StringValue': 'zone-alert'
                            }
                        },
                        MessageBody=(body)
                    )
                    print('send location alert for : {0}'.format(pet.name))

    except Exception as ex:
        print(ex)


def handle_zone_alert (event, context):
    try:
        for record in event['Records']:
            payload = json.loads(record['body'])
            pets = Pet.query(payload['owner'], Pet.name == payload['name'])
            subscriptions = [
                {
                    'endpoint': sub.endpoint,
                    'expiration_time': sub.expiration_time,
                    'keys': {
                        'p256dh': sub.keys.p256dh,
                        'auth': sub.keys.auth
                    }
                }
                for sub in PushSubscription.query(payload['owner'])
            ]
            for pet in pets:
                push_payload = {
                    'kind': 'zone-alert',
                    'args': {
                        'name': pet.name,
                        'picture': pet.picture,
                        'position': {
                            'lat': pet.location.position.lat,
                            'lng': pet.location.position.lng
                        }
                    }
                }
                for sub in subscriptions:
                    try:
                        print('key:')
                        print(os.environ.get('PUSH_KEY'))
                        webpush(
                            subscription_info=sub,
                            data=json.dumps(push_payload),
                            vapid_private_key=os.environ.get('PUSH_KEY'),
                            vapid_claims={
                                'sub': 'mailto:rasta.dev.01@gmail.com'
                            }
                        )
                    except WebPushException as ex:
                        print(ex)
                print('send notification for : {0}'.format(pet.name))

    except Exception as ex:
        print(ex)