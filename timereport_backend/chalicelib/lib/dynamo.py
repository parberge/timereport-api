import json

from dateutil import parser
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import logging
import ast

log = logging.getLogger(__name__)

dynamoboto = Dynamo.DynamoBoto

def get_id(user_id):
    try:
      response = dynamoboto.table.scan(user_id)
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
    log.info(f'event in create_event backend is {events}')
    # running curl_localhost sends this as string representation of dict
    if isinstance(events, str):
        events = ast.literal_eval(events)
    user_id = events.get('user_id')
    event_date = parser.parse(events.get('event_date'))
    user_name = events.get('user_name')
    reason = events.get('reason')
    hours = events.get('hours')

    event = Dynamo.EventModel(hash_key=user_id, range_key=event_date)
    event.user_name = user_name
    event.reason = reason
    event.hours = hours
    # save tables to database
    event.save()
