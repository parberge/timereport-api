import os
from chalice import Chalice
from chalicelib.lib import db
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


@app.route('/users', methods=['GET'], cors=True)
def list_users():
    return db.list_users()


@app.route('/users/{user_id}', methods=['GET'], cors=True)
def get_user(user_id):
    return db.get_user(user_id=user_id)


@app.route('/users/{user_id}/events', methods=['GET'], cors=True)
def list_all_events_by_user_id():
    return NotImplemented
    #return db.list_all_events_by_user_id()


@app.route('/users/{user_id}/events', methods=['DELETE'], cors=True)
def delete_all_events_by_user():
    return NotImplemented
    #return db.delete_all_events_by_user_id()


@app.route('/users/{user_id}/events/{date}', methods=['GET'], cors=True)
def get_event_by_user_id_and_date():
    return NotImplemented
    #return db.get_event_by_user_id_and_date()


@app.route('/users/{user_id}/events/{date}', methods=['DELETE'], cors=True)
def delete_event_by_user_id_and_date():
    return NotImplemented
    #return db.delete_event_by_user_id_and_date()


@app.route('/users/{user_id}/locks', methods=['GET'], cors=True)
def list_all_locks_by_user_id():
    return NotImplemented
    #return db.list_all_locks_by_user()


@app.route('/users/{user_id}/locks', methods=['DELETE'], cors=True)
def delete_all_locks_by_user_id():
    return NotImplemented
    #return db.delete_all_locks_by_user_id()


@app.route('/users/{user_id}/locks/{date}', methods=['GET'], cors=True)
def get_lock_by_user_id_and_date():
    return NotImplemented
    #return db.get_lock_by_user_id_and_date()


@app.route('/users/{user_id}/locks/{date}', methods=['DELETE'], cors=True)
def delete_lock_by_user_id_and_date():
    return NotImplemented
    #return db.delete_lock_by_user_id_and_date()


@app.route('/events', methods=['GET'], cors=True)
def list_all_events():
    return db.list_all_events()


@app.route('/events', methods=['POST'], cors=True)
def create_event():
    return db.create_event(app.current_request.json_body)


@app.route('/events/dates/{event_date}', methods=['GET'], cors=True)
def list_all_events_by_date(event_date):
    return db.list_all_events_by_date(event_date=event_date)


@app.route('/events/dates/{event_date}', methods=['DELETE'], cors=True)
def delete_all_events_by_date(event_date):
    return NotImplemented
    #return db.delete_all_events_by_date(event_date=event_date)


@app.route('/locks', methods=['GET'], cors=True)
def list_all_locks():
    return db.list_all_locks()


@app.route('/locks', methods=['POST'], cors=True)
def create_lock():
    db.create_lock(app.current_request.json_body)
    return app.current_request.json_body


@app.route('/locks/dates/{date}', methods=['GET'], cors=True)
def list_all_locks_by_date():
    return NotImplemented
    #return db.list_all_locks_by_date()


@app.route('/locks/dates/{event_date}', methods=['DELETE'], cors=True)
def delete_all_locks_by_date(event_date):
    return db.delete_all_locks_by_date(event_date)