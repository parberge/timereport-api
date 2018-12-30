import json

from dateutil import parser
from chalicelib.model import Dynamo
from botocore.exceptions import ClientError

db = Dynamo.EventModel
dynamoboto = Dynamo.DynamoBoto

# create the table
if not db.exists():
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

def get_id(user_id):
    return scan(user_id)

def get_user_between_date(user_id, start_date, end_date):
    pass

def create_event(events):
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

def scan(query):
    try:
      response = dynamoboto.table.scan(query)
    except ClientError as e:
      print(e.response['Error']['Message'])
    else:
      item = response['Items']
      print("GetItem succeeded:")
      return json.dumps(item, indent=4)
