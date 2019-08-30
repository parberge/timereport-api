import os
import boto3

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute



class EventModel(Model):
    """
    A DynamoDB Event Table
    """
    class Meta(object):
        table_name = os.getenv('DB_EVENT_TABLE_NAME', 'dev_event')
        host = os.getenv('DB_HOST', None)
        region = os.getenv('DB_REGION', 'eu-north-1')

    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)
    user_name = UnicodeAttribute()
    reason = UnicodeAttribute()
    hours = UnicodeAttribute()
    lock = BooleanAttribute(default=False)

class LockModel(Model):
    """
    A DynamoDB Lock model
    """
    class Meta(object):
        table_name = os.getenv('DB_LOCK_TABLE_NAME', 'dev_lock')
        host = os.getenv('DB_HOST', None)
        region = os.getenv('DB_REGION', 'eu-north-1')
    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)


class DynamoBotoEvent(EventModel.Meta):
    """
    A Boto3 DynamoDB resource
    """
    region = EventModel.Meta.region
    table_name = EventModel.Meta.table_name
    host = EventModel.Meta.host
    dynamodb = boto3.resource("dynamodb", region_name=region, endpoint_url=host)
    table = dynamodb.Table(table_name)

class DynamoBotoLock(LockModel.Meta):
    """
    A Boto3 DynamoDB resource
    """
    region = LockModel.Meta.region
    table_name = LockModel.Meta.table_name
    host = LockModel.Meta.host
    dynamodb = boto3.resource("dynamodb", region_name=region, endpoint_url=host)
    table = dynamodb.Table(table_name)