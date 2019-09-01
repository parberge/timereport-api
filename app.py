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


@app.route('/table-name', cors=True)
def test_name():
    """
    :return: table name
    """
    return {'name': [EventModel.Meta.table_name, LockModel.Meta.table_name]}


@app.route('/event', methods=['GET'], cors=True)
def get_all_events():
    return db_functions.get_all_events()


@app.route('/event/users', methods=['GET'], cors=True)
def get_user_ids():
    return db_functions.get_all_user_ids()


@app.route('/event/users/{user_id}', methods=['GET'], cors=True)
def get_all_events_by_user_id(user_id):
    return db_functions.get_all_events_by_user_id(user_id=user_id)


@app.route('/event/users/{user_id}/{event_date}', methods=['GET'], cors=True)
def delete_event(user_id, event_date):
    return db_functions.get_event_by_user_id_and_date(user_id=user_id, event_date=event_date)


@app.route('/event/users/{user_id}/{event_date}', methods=['DELETE'], cors=True)
def delete_event(user_id, event_date):
    return db_functions.delete_event(user_id=user_id, event_date=event_date)


@app.route('/event/date/{event_date}', methods=['GET'], cors=True)
def get_events_by_date(event_date):
    return db_functions.get_all_events_by_date(event_date=event_date)


@app.route('/event', methods=['POST'], cors=True)
def create_event():
    return db_functions.create_event(app.current_request.json_body)


@app.route('/lock', methods=['GET'], cors=True)
def get_all_locks():
    return db_functions.get_all_locks()


@app.route('/lock/users/{user_id}/{event_date}', methods=['GET'], cors=True)
def get_lock(user_id, event_date):
    return db_functions.get_lock(user_id=user_id, event_date=event_date)


@app.route('/lock', methods=['POST'], cors=True)
def create_lock():
    db_functions.create_lock(app.current_request.json_body)
    return app.current_request.json_body


@app.route('/lock/users/{user_id}/{event_date}', methods=['DELETE'], cors=True)
def delete_lock(user_id, event_date):
    return db_functions.delete_lock(user_id, event_date)


@app.route('/lock/date/{event_date}', methods=['DELETE'], cors=True)
def delete_all_locks_by_date(event_date):
    return db_functions.delete_all_locks_by_date(event_date)