import os

from dateutil import parser
from chalicelib.model import Dynamo

db = Dynamo.EventModel

#db.Meta.aws_access_key_id = os.getenv('AWS_ACCESS_KEY', 'my_access_key_id')
#db.Meta.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'my_secret_access_key')

# create the table
if not db.exists():
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

def get_id(user_id):
    the_list = []
    for i in db.scan(db.user_id == user_id):
        the_list.append(i.attribute_values)
    return the_list

def get_user_between_date(user_id, start_date, end_date):
    result = []
    for i in db.scan((db.user_id == user_id) & (db.event_date.between(start_date, end_date))):
        result.append(i.attribute_values)
    return result

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

