import json

from dateutil import parser
from chalicelib.model import Dynamo
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key
import logging
import ast

log = logging.getLogger(__name__)

dynamoboto = Dynamo.DynamoBoto

def get_id(user_id):
    try:
      response = dynamoboto.table.scan(FilterExpression=Key('user_id').eq(user_id))
    except ClientError as e:
      log.debug(e.response['Error']['Message'])
    else:
      item = response['Items']
      log.debug("GetItem succeeded:")
      return json.dumps(item, indent=4)

def get_user_between_date(user_id, start_date, end_date):
    try:
        response = dynamoboto.table.scan(FilterExpression=Attr('event_date').between(start_date, end_date)
                                       & Attr('user_id').eq(user_id)
                                       )
    except ClientError as e:
        log.debug(e.response['Error']['Message'])
    else:
        item = response['Items']
        log.debug(f"GetItem succeeded: {item}")
        return json.dumps(item, indent=4)

def create_event(events):
    log.debug(f'event in create_event backend is {events}')
    # running curl_localhost sends this as string representation of dict
    if isinstance(events, str):
        events = ast.literal_eval(events)
    user_id = events.get('user_id')
    event_date = events.get('event_date')
    user_name = events.get('user_name')
    reason = events.get('reason')
    hours = events.get('hours')
    log.info(f'event_date is {event_date}')
    event = Dynamo.EventModel(hash_key=user_id, range_key=event_date)
    event.user_name = user_name
    event.reason = reason
    event.hours = hours
    # save tables to database
    event.save()

def delete_event(user_id, date):
    try:
      response = dynamoboto.table.delete_item(Key={'event_date':date, 'user_id':user_id})
    except ClientError as e:
      log.debug(e.response['Error']['Message'])
    else:
      item = response['Items']
      log.debug("Delete item succeeded:")
      return json.dumps(item, indent=4)
