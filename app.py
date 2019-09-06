import os
from chalice import Chalice
from chalicelib.lib import db
from chalicelib.model.models import EventModel, LockModel
import logging


app = Chalice(app_name='timereport_backend')
app.debug = os.getenv('BACKEND_DEBUG', False)
log = logging.getLogger(__name__)


for db_instance in [EventModel, LockModel]:
    if not db_instance.exists():
        db_instance.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@app.route('/table-names', cors=True)
def test_name():
    """
    :return: table name
    """
    return {'name': [EventModel.Meta.table_name, LockModel.Meta.table_name]}


@app.route('/users', methods=['GET'], cors=True)
def list_users():
    """
    Method
    GET    /users
    Return list of all users
    """
    return db.list_users()


@app.route('/users/{user_id}', methods=['GET'], cors=True)
def get_user(user_id):
    """
    Method
    GET    /users/<user_id>
    Return a single user
    """
    return db.get_user(user_id)


@app.route('/users/{user_id}/events', methods=['GET'], cors=True)
def list_events_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/events
    Return a list of all user_id's events
    """
    return db.list_events_by_user_id(user_id)


@app.route('/users/{user_id}/events', methods=['DELETE'], cors=True)
def delete_all_events_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/events
    Delete all the user_id's events
    """
    return db.delete_all_events_by_user_id(user_id)


@app.route('/users/{user_id}/locks', methods=['GET'], cors=True)
def list_locks_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/locks
    Return a list of user_id's locks
    """
    return db.list_locks_by_user_id(user_id)


@app.route('/users/{user_id}/locks', methods=['DELETE'], cors=True)
def delete_all_locks_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/locks
    Delete all locks for user_id
    """
    return db.delete_all_locks_by_user_id(user_id)


@app.route('/users/{user_id}/locks/{event_date}', methods=['DELETE'], cors=True)
def delete_lock_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/locks/<date>
    Delete user_id lock on date
    """
    return db.delete_lock_by_user_id_and_date(user_id, event_date)


@app.route('/users/{user_id}/events/{event_date}', methods=['GET'], cors=True)
def get_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    GET    /users/<user_id>/events/<date>
    Return event for user_id on date
    """
    return db.get_event_by_user_id_and_date(user_id, event_date)


@app.route('/users/{user_id}/events/{event_date}', methods=['DELETE'], cors=True)
def delete_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/events/<date>
    Delete user_id's event on date
    """
    return db.delete_event_by_user_id_and_date(user_id, event_date)


@app.route('/events', methods=['POST'], cors=True)
def create_event():
    """
    Method
    POST    /events
    Create event
    data: {"user_id":"foo01","user_name":"Foo Bar","reason":"sick","event_date":"2019-03-21","hours":8}
    """
    return db.create_event(app.current_request.json_body)


@app.route('/events', methods=['GET'], cors=True)
def list_all_events():
    """
    Method
    GET    /events
    Returns list of all events
    """
    return db.list_all_events()


@app.route('/events/dates/{event_date}', methods=['GET'], cors=True)
def list_all_events_by_date(event_date):
    """
    Method
    GET    /events/dates/<date>
    Returns list of all events on date
    """
    return db.list_all_events_by_date(event_date)


@app.route('/events/dates/{event_date}', methods=['DELETE'], cors=True)
def delete_all_events_by_date(event_date):
    """
    Method
    DELETE    /events/dates/<date>
    Delete all events on date
    """
    return db.delete_all_events_by_date(event_date)


@app.route('/locks', methods=['POST'], cors=True)
def create_lock():
    """
    Method
    POST    /locks
    Create lock
    data: {"user_id":"foo01","event_date":"2019-02"}
    """
    db.create_lock(app.current_request.json_body)
    return app.current_request.json_body


@app.route('/locks', methods=['GET'], cors=True)
def list_all_locks():
    """
    Method
    GET    /locks
    Returns list of all locks
    """
    return db.list_all_locks()


@app.route('/locks/dates/{event_date}', methods=['GET'], cors=True)
def list_all_locks_by_date(event_date):
    """
    Method
    GET    /locks/dates/<date>
    Returns list of all locks on date
    """
    return db.list_all_locks_by_date(event_date)


@app.route('/locks/dates/{event_date}', methods=['DELETE'], cors=True)
def delete_all_locks_by_date(event_date):
    """
    Method
    DELETE    /locks/dates/<date>
    Delete all locks on date
    """
    return db.delete_all_locks_by_date(event_date)