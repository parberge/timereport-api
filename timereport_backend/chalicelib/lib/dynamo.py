import os

from chalicelib.model import Dynamo

db = Dynamo.EventModel
db.Meta.host = os.getenv('DB_URL', 'http://127.0.0.1:8000')

# create the table
if not db.exists():
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


def get_user_by_id(user_id):
    result = []
    for i in db.scan((db.user_id == user_id)):
        result.append(i.attribute_values)
    return result

def get_user_between_date(user_id, start_date, end_date):
    result = []
    for i in db.scan((db.user_id == user_id) & (db.event_date.between(start_date, end_date))):
        result.append(i.attribute_values)
    return result

def create_event(events):
    for e in events:
        user_id = e.get('user_id')
        event_date = e.get('event_date')
        user_name = e.get('user_name')
        reason = e.get('reason')
        hours = e.get('hours')

        event = Dynamo.EventModel(hash_key=user_id, range_key=event_date)
        event.user_name = user_name
        event.reason = reason
        event.hours = hours
        # save tables to database
        event.save()

