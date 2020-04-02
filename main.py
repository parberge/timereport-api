import os
from flask import Flask
from flask_cors import CORS
from chalicelib.lib import db_v1, db_v2
from chalicelib.model.models import EventTable, LockTable
import logging


app = Flask("timereport_backend")
CORS(app)
app.debug = os.environ.get("BACKEND_DEBUG", False)
port = int(os.environ.get("PORT", 8080))
log_level = logging.DEBUG if app.debug else logging.INFO
app.logger.setLevel(log_level)


for db_instance in [EventTable, LockTable]:
    if not db_instance.exists():
        db_instance.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


@app.route("/table-names")
def test_name():
    """
    :return: table name
    """
    return {"name": [EventTable.Meta.table_name, LockTable.Meta.table_name]}


@app.route("/users", methods=["GET"])
def list_users():
    """
    Method
    GET    /users
    Return list of all users
    """
    return db_v2.list_users()


@app.route("/users/{user_id}", methods=["GET"])
def get_user(user_id):
    """
    Method
    GET    /users/<user_id>
    Return a single user
    """
    return db_v2.get_user(user_id)


@app.route("/users/{user_id}/events", methods=["GET"])
def list_events_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/events
    :params from: str, to: str
      filter on date range
    Return a list of all user_id's events
    """
    if app.current_request.query_params:
        date_from = app.current_request.query_params.get("from")
        date_to = app.current_request.query_params.get("to")
        return db_v2.list_events_by_user_id(user_id, date_from, date_to)
    return db_v2.list_events_by_user_id(user_id)


@app.route("/users/{user_id}/events", methods=["DELETE"])
def delete_all_events_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/events
    Delete all the user_id's events
    """
    return db_v2.delete_all_events_by_user_id(user_id)


@app.route("/users/{user_id}/locks", methods=["GET"])
def list_locks_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/locks
    Return a list of user_id's locks
    """
    return db_v2.list_locks_by_user_id(user_id)


@app.route("/users/{user_id}/locks", methods=["DELETE"])
def delete_all_locks_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/locks
    Delete all locks for user_id
    """
    return db_v2.delete_all_locks_by_user_id(user_id)


@app.route("/users/{user_id}/locks/{event_date}", methods=["DELETE"])
def delete_lock_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/locks/<date>
    Delete user_id lock on date
    """
    return db_v2.delete_lock_by_user_id_and_date(user_id, event_date)


@app.route("/users/{user_id}/events/{event_date}", methods=["DELETE"])
def delete_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/events/<date>
    Delete user_id's event on date
    """
    return db_v2.delete_event_by_user_id_and_date(user_id, event_date)


@app.route("/users/{user_id}/events/{event_date}", methods=["GET"])
def get_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/events/<date>
    Delete user_id's event on date
    """
    return db_v2.get_event_by_user_id_and_date(user_id, event_date)


@app.route("/events", methods=["POST"])
def create_event_v2():
    """
    Method
    POST    /events
    Create event
    data: {"user_id":"foo01","user_name":"Foo Bar","reason":"sick","event_date":"2019-03-21","hours":8}
    """
    return db_v2.create_event_v2(app.current_request.json_body)


@app.route("/events", methods=["GET"])
def list_all_events():
    """
    Method
    GET    /events
    Returns list of all events
    """
    return db_v2.list_all_events()


@app.route("/events/dates/{event_date}", methods=["GET"])
def list_all_events_by_date(event_date):
    """
    Method
    GET    /events/dates/<date>
    Returns list of all events on date
    """
    return db_v2.list_all_events_by_date(event_date)


@app.route("/events/dates/{event_date}", methods=["DELETE"])
def delete_all_events_by_date(event_date):
    """
    Method
    DELETE    /events/dates/<date>
    Delete all events on date
    """
    return db_v2.delete_all_events_by_date(event_date)


@app.route("/locks", methods=["POST"])
def create_locks():
    """
    Method
    POST    /locks
    Create lock
    data: {"user_id":"foo01","event_date":"2019-02"}
    """
    db_v2.create_lock(app.current_request.json_body)
    return app.current_request.json_body


@app.route("/locks", methods=["GET"])
def list_all_locks():
    """
    Method
    GET    /locks
    Returns list of all locks
    """
    return db_v2.list_all_locks()


@app.route("/locks/dates/{event_date}", methods=["GET"])
def list_all_locks_by_date(event_date):
    """
    Method
    GET    /locks/dates/<date>
    Returns list of all locks on date
    """
    return db_v2.list_all_locks_by_date(event_date)


@app.route("/locks/dates/{event_date}", methods=["DELETE"])
def delete_all_locks_by_date(event_date):
    """
    Method
    DELETE    /locks/dates/<date>
    Delete all locks on date
    """
    return db_v2.delete_all_locks_by_date(event_date)


##################################################
#                                                #
#      TODO: The following code is support for   #
#            v1 api-calls and will be removed    #
#                                                #
##################################################


@app.route("/event/users", methods=["GET"])
def get_user_ids():
    return db_v2.list_users()


@app.route("/event/users/{user_id}", methods=["GET"])
def get_events_by_user_id(user_id):
    start_date = None
    end_date = None
    if app.current_request.query_params:
        app.logger.debug(f"Got request params: {app.current_request.query_params}")
        start_date = app.current_request.query_params.get("startDate")
        end_date = app.current_request.query_params.get("endDate")

    return db_v1.get_id(user_id=user_id, start_date=start_date, end_date=end_date)


@app.route("/event/users/{user_id}", methods=["POST"])
def create_event_v1(user_id):
    """
    :param user_id:
    :return:
    """
    return db_v1.create_event_v1(app.current_request.json_body, user_id)


@app.route("/event/users/{user_id}", methods=["DELETE"])
def delete_event_by_id(user_id):
    """
    :param user_id:
    :return:
    """
    if app.current_request.query_params:
        start_date = app.current_request.query_params.get("date")
        app.logger.info(
            f"delete event backend: date is {start_date} and id is {user_id}"
        )
        return db_v1.delete_event_v1(user_id, start_date)


@app.route("/lock/users/{user_id}/{event_date}", methods=["GET"])
def get_lock(user_id, event_date):
    """
    :param user_id:
    :param event_date:
    :return:
    """
    return db_v2.get_lock_by_user_id_and_date(user_id=user_id, event_date=event_date)


@app.route("/lock", methods=["POST"])
def create_lock():
    db_v2.create_lock(app.current_request.json_body)
    return app.current_request.json_body


if __name__ == "__main__":
    app.run(host="127.0.0.1")
