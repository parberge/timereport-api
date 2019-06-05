import os
from chalice import Chalice
from chalicelib.lib import dynamo
from chalicelib.model import Dynamo
import logging


app = Chalice(app_name='timereport_backend')
app.debug = os.getenv('BACKEND_DEBUG', False)
log = logging.getLogger(__name__)

db = Dynamo.EventModel
# create the table
if not db.exists():
    log.info('database table do not exist, creating it')
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


@app.route('/table-name', cors=True)
def test_name():
    """
    :return: table name
    """
    return {'name': dynamo.dynamoboto.table.name }


@app.route('/event/users', methods=['GET'], cors=True)
def get_user_ids():
    return dynamo.get_user_ids()


@app.route('/event/users/{user_id}', methods=['GET'], cors=True)
def get_events_by_user_id(user_id):
    start_date = None
    end_date = None
    if app.current_request.query_params:
        log.debug(f"Got request params: {app.current_request.query_params}")
        start_date = app.current_request.query_params.get('startDate')
        end_date = app.current_request.query_params.get('endDate')

    return dynamo.get_id(user_id=user_id, start_date=start_date, end_date=end_date)


@app.route('/event/users/{user_id}', methods=['POST'], cors=True)
def create_event(user_id):
    dynamo.create_event(app.current_request.json_body, user_id)
    return app.current_request.json_body


@app.route('/event/users/{user_id}', methods=['DELETE'], cors=True)
def delete_event_by_id(user_id):
    if app.current_request.query_params:
        start_date = app.current_request.query_params.get('date')
        app.log.info(f'delete event backend: date is {start_date} and id is {user_id}')
        return dynamo.delete_event(user_id, start_date)
