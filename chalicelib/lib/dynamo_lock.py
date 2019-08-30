import json

from dateutil import parser
from chalicelib.model import Dynamo
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key
import logging
import ast

log = logging.getLogger(__name__)

dynamoboto = Dynamo.DynamoBotoLock

def create_lock(lock_request):
    log.debug(f'lock_request: {lock_request}')
    # running curl_localhost sends this as string representation of dict
    event_date = lock_request.get('event_date')
    user_id = lock_request.get('user_id')
    lock = Dynamo.LockModel(hash_key=user_id, range_key=event_date)
    lock.save()

def get_lock(user_id, event_date):
    log.info(f'inside delete_event in dynamo backend: user_id is {user_id}, date is {event_date}')
    expression = Attr('event_date').eq(event_date) & Attr('user_id').eq(user_id)
    try:
      response = dynamoboto.table.scan(FilterExpression=expression)
    except ClientError as e:
      log.debug(e.response['Error']['Message'])
    else:
      log.debug(f"Delete item succeeded with response: {response}")
      return json.dumps(response, indent=4)

def get_id(user_id, event_date):
    """
    Get items for user. Optionally between start and end date.
    """
    expression = Attr('event_date').eq(event_date) & Attr('user_id').eq(user_id)

    try:
      response = dynamoboto.table.scan(FilterExpression=expression)
    except ClientError as e:
      log.debug(e.response['Error']['Message'])
    else:
      item = response['Items']
      log.debug("GetItem succeeded:")
      return json.dumps(item, indent=4)