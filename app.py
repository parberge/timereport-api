import os
from chalice import Chalice
from chalicelib.lib import db_functions
from chalicelib.model.models import EventModel, LockModel
import logging


app = Chalice(app_name='timereport_backend')
app.debug = os.getenv('BACKEND_DEBUG', False)
log = logging.getLogger(__name__)


for db in [EventModel, LockModel]:
    if not db.exists():
        db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@app.route('/table-names', cors=True)
def test_name():
    """
    :return: table name
    """
    return {'name': [EventModel.Meta.table_name, LockModel.Meta.table_name]}


@app.route('/events', methods=['GET'], cors=True)
def get_all_events():
    return db_functions.get_all_events()


@app.route('/events/users', methods=['GET'], cors=True)
def get_user_ids():
    return db_functions.get_all_user_ids()


@app.route('/events/users/{user_id}', methods=['GET'], cors=True)
def get_all_events_by_user_id(user_id):
    return db_functions.get_all_events_by_user_id(user_id=user_id)


@app.route('/events/users/{user_id}/{event_date}', methods=['GET'], cors=True)
def delete_event(user_id, event_date):
    return db_functions.get_event_by_user_id_and_date(user_id=user_id, event_date=event_date)


@app.route('/events/users/{user_id}/{event_date}', methods=['DELETE'], cors=True)
def delete_event(user_id, event_date):
    return db_functions.delete_event(user_id=user_id, event_date=event_date)


@app.route('/events/dates/{event_date}', methods=['GET'], cors=True)
def get_events_by_date(event_date):
    return db_functions.get_all_events_by_date(event_date=event_date)


@app.route('/events', methods=['POST'], cors=True)
def create_event():
    return db_functions.create_event(app.current_request.json_body)


@app.route('/locks', methods=['GET'], cors=True)
def get_all_locks():
    return db_functions.get_all_locks()


@app.route('/locks/users/{user_id}/{event_date}', methods=['GET'], cors=True)
def get_lock(user_id, event_date):
    return db_functions.get_lock(user_id=user_id, event_date=event_date)


@app.route('/locks', methods=['POST'], cors=True)
def create_lock():
    db_functions.create_lock(app.current_request.json_body)
    return app.current_request.json_body


@app.route('/locks/users/{user_id}/{event_date}', methods=['DELETE'], cors=True)
def delete_lock(user_id, event_date):
    return db_functions.delete_lock(user_id, event_date)


@app.route('/locks/dates/{event_date}', methods=['DELETE'], cors=True)
def delete_all_locks_by_date(event_date):
    return db_functions.delete_all_locks_by_date(event_date)