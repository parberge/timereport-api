import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute


class EventTable(Model):
    """
    A DynamoDB Event Table
    """
    class Meta(object):
        table_name = os.getenv('DB_EVENT_TABLE_NAME', 'dev_event')
        host = os.getenv('DB_HOST', "http://localhost:8000")
        region = os.getenv('DB_REGION', 'eu-north-1')

    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)
    user_name = UnicodeAttribute()
    reason = UnicodeAttribute()
    hours = UnicodeAttribute()


class LockTable(Model):
    """
    A DynamoDB Lock model
    """
    class Meta(object):
        table_name = os.getenv('DB_LOCK_TABLE_NAME', 'dev_lock')
        host = os.getenv('DB_HOST', "http://localhost:8000")
        region = os.getenv('DB_REGION', 'eu-north-1')
    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)