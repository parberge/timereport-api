import ast
import json
import logging

from chalicelib.model.models import EventTable

log = logging.getLogger(__name__)


################################################
#                                              #
#                    API v1                    #
#                                              #
################################################


def get_id(user_id, start_date=None, end_date=None):
    """
    Get items for user. Optionally between start and end date.
    Status: Implemented
    """
    events = []
    if start_date and end_date:
        for event in EventTable.scan(
                (EventTable.event_date.between(start_date, end_date))
                & (EventTable.user_id == user_id)
        ):
            events.append(event.attribute_values)
    else:
        event = EventTable.scan(EventTable.user_id == user_id)
        for e in event:
            events.append(e.attribute_values)

    return json.dumps(events)


def create_event_v1(events, user_id):
    """
    :param events:
    :param user_id=None
    :return: status
    """
    if isinstance(events, str):
        events = ast.literal_eval(events)
    event = EventTable(
        user_id=user_id,
        event_date=f"{events.get('event_date')}",
        user_name=f"{events.get('user_name')}",
        reason=f"{events.get('reason')}",
        hours=f"{events.get('hours')}",
    )
    return json.dumps(event.save())


def delete_event_v1(user_id, date):
    log.info(f'inside delete_event in dynamo backend: user_id is {user_id}, date is {date}')
    events = EventTable.scan(
        (EventTable.user_id == user_id)
        & (EventTable.event_date == date))
    for event in events:
        event.delete()
    return json.dumps({"Method": f"DELETE", "user_id": f"{user_id}", "Status": "OK"})
