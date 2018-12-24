import os

from dateutil import parser
from chalicelib.model import Dynamo

db = Dynamo.EventModel
db.Meta.host = os.getenv('DB_URL', 'http://127.0.0.1:8000')
# create the table
if not db.exists():
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

def get_id(user_id):
    for i in db.scan((db.user_id == user_id)):
        return i.attribute_values

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

