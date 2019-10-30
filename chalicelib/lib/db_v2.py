import ast
import json
import logging
from datetime import datetime

from botocore.exceptions import ClientError

from chalicelib.lib.helpers import date_range
from chalicelib.model.models import LockTable, EventTable

log = logging.getLogger(__name__)


################################################
#                                              #
#                    API v2                    #
#                                              #
################################################


def list_users():
    """
    returns list of all users
    """
    user_ids = {}
    for item in EventTable.scan():
        if item.user_id not in user_ids:
            user_ids[item.user_id] = item.user_name
    return json.dumps(user_ids)


def get_user(user_id):
    """
    returns user_id or empty
    """
    for user in EventTable.scan(EventTable.user_id == user_id):
        return json.dumps({"message": f"{user_id} exists", "status": "OK"})
    return json.dumps({"message": f"{user_id} does not exist", "status": "NOT FOUND"})


def list_events_by_user_id(user_id, date_from=None, date_to=None):
    """
    :param user_id:
    :param date_from: optional
    :param date_to: optional
    :return: list of events for user_id
    """
    events = []

    format_str = "%Y-%m-%d"

    if not date_from and not date_to:
        for event in EventTable.scan(EventTable.user_id == user_id):
            events.append(event.attribute_values)
        return json.dumps(events)
    else:
        datetime_from = datetime.strptime(date_from, format_str)
        datetime_to = datetime.strptime(date_to, format_str)
        for d in date_range(datetime_from, datetime_to):
            for event in EventTable.scan(
                (EventTable.user_id == user_id)
                & (EventTable.event_date == d.strftime(format_str))
            ):
                events.append(event.attribute_values)
        return events


def delete_all_events_by_user_id(user_id):
    """
    :param user_id:
    :return: status
    """
    events = EventTable.scan(EventTable.user_id == user_id)
    for event in events:
        event.delete()
    return json.dumps({"Method": f"DELETE", "user_id": f"{user_id}", "Status": "OK"})


def get_event_by_user_id_and_date(user_id, event_date):
    """
    :param user_id:
    :param event_date:
    :return: event
    """
    try:
        e = EventTable.get(user_id, event_date)
        return e.attribute_values
    except EventTable.DoesNotExist as e:
        return json.dumps({})


def delete_event_by_user_id_and_date(user_id, event_date):
    """
    :param user_id:
    :param event_date:
    :return: method, user_id, count, status
    """
    count = 0
    events = EventTable.scan(
        (EventTable.user_id == user_id) & (EventTable.event_date == event_date)
    )
    for event in events:
        event.delete()
        count += 1
    return json.dumps(
        {
            "method": f"delete",
            "user_id": f"{user_id}",
            "count": f"{count}",
            "date": f"{event_date}",
            "status": "ok",
        }
    )


def list_locks_by_user_id(user_id):
    """
    :param user_id:
    :return: list of locks for user
    """
    locks = []
    for lock in LockTable.scan(LockTable.user_id == user_id):
        locks.append(lock.attribute_values)
    return json.dumps(locks)


def delete_all_locks_by_user_id(user_id):
    """
    :param user_id:
    :return: method, user_id, count, status
    """
    count = 0
    for lock in LockTable.scan(LockTable.user_id == user_id):
        lock.delete()
        count += 1
    return json.dumps(
        {
            "method": f"delete",
            "user_id": f"{user_id}",
            "count": f"{count}",
            "status": "ok",
        }
    )


def get_lock_by_user_id_and_date(user_id, event_date):
    """
    :param user_id:
    :param event_date:
    :return: lock for user
    """
    scan = LockTable.scan(
        (LockTable.user_id == user_id) & (LockTable.event_date == event_date)
    )
    locks = []
    for lock in scan:
        locks.append(lock.attribute_values)
    return json.dumps(locks)


def delete_lock_by_user_id_and_date(user_id, event_date):
    """
    :param user_id:
    :param event_date:
    :return: status
    """
    locks = LockTable.scan(
        (LockTable.user_id == user_id) & (LockTable.event_date == event_date)
    )
    for lock in locks:
        lock.delete()
    return json.dumps(
        {
            "Method": f"DELETE",
            "user_id": f"{user_id}",
            "date": f"{event_date}",
            "Status": "OK",
        }
    )


def list_all_events():
    """
    :return: list of all events
    """
    events = []
    for event in EventTable.scan():
        events.append(event.attribute_values)
    return json.dumps(events)


def list_all_events_by_date(event_date):
    """
    :param event_date:
    :return: list of all events for date
    """
    events = []
    for event in EventTable.scan(EventTable.event_date == event_date):
        events.append(event.attribute_values)
    return json.dumps(events)


def create_event_v2(events):
    """
    :param events:
    :return: status
    """
    if isinstance(events, str):
        events = ast.literal_eval(events)
    event = EventTable(
        user_id=f"{events.get('user_id')}",
        event_date=f"{events.get('event_date')}",
        user_name=f"{events.get('user_name')}",
        reason=f"{events.get('reason')}",
        hours=f"{events.get('hours')}",
    )
    return json.dumps(event.save())


def delete_all_events_by_date(event_date):
    """
    :param event_date:
    :return: status
    """
    events = EventTable.scan(EventTable.event_date == event_date)
    for event in events:
        event.delete()
    return json.dumps({"Method": f"DELETE", "date": f"{event_date}", "Status": "OK"})


def list_all_locks():
    """
    :return: list of all locks
    """
    locks = []
    for lock in LockTable.scan():
        locks.append(lock.attribute_values)
    return json.dumps(locks)


def create_lock(lock_request):
    """
    :param lock_request:
    :return: status
    """
    try:
        lock = LockTable(
            hash_key=f"{lock_request.get('user_id')}",
            range_key=f"{lock_request.get('event_date')}",
        )
        return json.dumps(lock.save())
    except ClientError as e:
        log.debug(e.response["Error"]["Message"])
        return json.dumps({"error": "Failed to create lock"})


def list_all_locks_by_date(event_date):
    """
    :param event_date:
    :return: list of locks for date
    """
    locks = []
    for lock in LockTable.scan(LockTable.event_date == event_date):
        locks.append(lock.attribute_values)
    return json.dumps(locks)


def delete_all_locks_by_date(event_date):
    """
    :param event_date:
    :return: status
    """
    locks = LockTable.scan(LockTable.event_date == event_date)
    for lock in locks:
        lock.delete()
    return json.dumps({"Method": f"DELETE", "date": f"{event_date}", "Status": "OK"})
