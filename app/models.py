# coding: utf-8

import os
from datetime import datetime
from pynamodb.attributes import UnicodeAttribute, MapAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class Position(MapAttribute):
    lat = NumberAttribute(null=False)
    lng = NumberAttribute(null=False)

class Zone(MapAttribute):
    position = Position(null=False)
    radius = NumberAttribute(null=False)

class PetLocation(MapAttribute):
    position = Position(null=False)
    at = NumberAttribute(null=False, default=lambda: datetime.timestamp(datetime.now()))


class Pet(Model):
    class Meta:
        table_name = os.environ.get('PET_TABLE', 'pet')
        region = os.environ.get('PROVIDER_REGION', 'eu-central-1')
        
    id = UnicodeAttribute(null=False)
    created_at = NumberAttribute(null=False, default=lambda: datetime.timestamp(datetime.now()))
    owner = UnicodeAttribute(hash_key=True, null=False)
    name = UnicodeAttribute(range_key=True, null=False)
    serial = UnicodeAttribute(null=False)
    picture = UnicodeAttribute(null=False)
    description = UnicodeAttribute(null=False)
    location = PetLocation(null=False)
    zone = Zone(null=False)


class PushKey(MapAttribute):
    p256dh = UnicodeAttribute(null=False)
    auth = UnicodeAttribute(null=False)


class PushSubscription(Model):
    class Meta:
        table_name = os.environ.get('SUBSCRIPTION_TABLE', 'subscription')
        region = os.environ.get('DB_REGION', 'eu-central-1')
    
    owner = UnicodeAttribute(hash_key=True, null=False)
    endpoint = UnicodeAttribute(range_key=True, null=False)
    created_at = UTCDateTimeAttribute(null=False, default=datetime.now)
    expiration_time = NumberAttribute(null=True)
    keys = PushKey(null=False)