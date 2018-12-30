import os
import boto3

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute



class EventModel(Model):
    """
    A DynamoDB Event Table
    """
    class Meta(object):
        table_name = os.getenv('DB_TABLE_NAME', 'event')
        region = os.getenv('DB_REGION', 'eu-north-1')

    user_id = UnicodeAttribute(hash_key=True)
    event_date = UTCDateTimeAttribute(range_key=True)
    user_name = UnicodeAttribute()
    reason = UnicodeAttribute()
    hours = UnicodeAttribute()

class DynamoBoto(EventModel.Meta):
    """
    A Boto3 DynamoDB resource
    """
    region = EventModel.Meta.region
    table_name = EventModel.Meta.table_name

    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)


