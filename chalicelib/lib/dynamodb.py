import ast
import json
import logging
import os
from datetime import datetime
from botocore.exceptions import ClientError
from chalicelib.lib.helpers import date_range
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

log = logging.getLogger(f"timereport_backend.{__name__}")


class DynamodbHandler:
    def __init__(self):
        """
        Setup DB engine
        """
        for db_instance in [EventTable, LockTable]:
            if not db_instance.exists():
                db_instance.create_table(
                    read_capacity_units=1, write_capacity_units=1, wait=True
                )

    def get_tables(self):
        return {"name": [EventTable.Meta.table_name, LockTable.Meta.table_name]}

    def list_users(self):
        """
        returns list of all users
        """
        user_ids = {}
        for item in EventTable.scan():
            if item.user_id not in user_ids:
                user_ids[item.user_id] = item.user_name
        return json.dumps(user_ids)

    def get_user(self, user_id):
        """
        returns user_id or empty
        """
        for user in EventTable.scan(EventTable.user_id == user_id):
            return json.dumps({"message": f"{user_id} exists", "status": "OK"})
        return json.dumps(
            {"message": f"{user_id} does not exist", "status": "NOT FOUND"}
        )

    def list_events_by_user_id(self, user_id, date_from=None, date_to=None):
        """
        :param user_id:
        :param date_from: optional
        :param date_to: optional
        :return: list of events for user_id
        """
        events = []

        if not date_from and not date_to:
            for event in EventTable.query(user_id):
                events.append(event.attribute_values)
            return json.dumps(events)
        else:
            for event in EventTable.query(
                user_id,
                range_key_condition=EventTable.event_date.between(date_from, date_to),
            ):
                events.append(event.attribute_values)
            return events

    def delete_all_events_by_user_id(self, user_id):
        """
        :param user_id:
        :return: status
        """
        events = EventTable.scan(EventTable.user_id == user_id)
        for event in events:
            event.delete()
        return json.dumps(
            {"Method": f"DELETE", "user_id": f"{user_id}", "Status": "OK"}
        )

    def get_event_by_user_id_and_date(self, user_id, event_date):
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

    def delete_event_by_user_id_and_date(self, user_id, event_date):
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

    def list_locks_by_user_id(self, user_id):
        """
        :param user_id:
        :return: list of locks for user
        """
        locks = []
        for lock in LockTable.scan(LockTable.user_id == user_id):
            locks.append(lock.attribute_values)
        return json.dumps(locks)

    def delete_all_locks_by_user_id(self, user_id):
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

    def get_lock_by_user_id_and_date(self, user_id, event_date):
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

    def delete_lock_by_user_id_and_date(self, user_id, event_date):
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

    def list_all_events(self):
        """
        :return: list of all events
        """
        events = []
        for event in EventTable.scan():
            events.append(event.attribute_values)
        return json.dumps(events)

    def list_all_events_by_date(self, event_date):
        """
        :param event_date:
        :return: list of all events for date
        """
        events = []
        for event in EventTable.scan(EventTable.event_date == event_date):
            events.append(event.attribute_values)
        return json.dumps(events)

    def create_event_v2(self, events):
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

    def delete_all_events_by_date(self, event_date):
        """
        :param event_date:
        :return: status
        """
        events = EventTable.scan(EventTable.event_date == event_date)
        for event in events:
            event.delete()
        return json.dumps(
            {"Method": f"DELETE", "date": f"{event_date}", "Status": "OK"}
        )

    def list_all_locks(self):
        """
        :return: list of all locks
        """
        locks = []
        for lock in LockTable.scan():
            locks.append(lock.attribute_values)
        return json.dumps(locks)


def create_lock(self, lock_request):
    """
    :param lock_request:
    :return: status
    """
    log.info(f"Lock request: {lock_request}")
    try:
        lock = LockTable(
            hash_key=f"{lock_request.get('user_id')}",
            range_key=f"{lock_request.get('event_date')}",
        )
        return json.dumps(lock.save())
    except ClientError as e:
        log.debug(e.response["Error"]["Message"])
        return json.dumps({"error": "Failed to create lock"})

    def list_all_locks_by_date(self, event_date):
        """
        :param event_date:
        :return: list of locks for date
        """
        locks = []
        for lock in LockTable.scan(LockTable.event_date == event_date):
            locks.append(lock.attribute_values)
        return json.dumps(locks)

    def delete_all_locks_by_date(self, event_date):
        """
        :param event_date:
        :return: status
        """
        locks = LockTable.scan(LockTable.event_date == event_date)
        for lock in locks:
            lock.delete()
        return json.dumps(
            {"Method": f"DELETE", "date": f"{event_date}", "Status": "OK"}
        )


class EventTable(Model):
    """
    A DynamoDB Event Table
    """

    class Meta(object):
        table_name = os.getenv("DB_EVENT_TABLE_NAME", "dev_event")
        host = os.getenv("DB_HOST", None)
        region = os.getenv("DB_REGION", "eu-north-1")

    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)
    user_name = UnicodeAttribute()
    reason = UnicodeAttribute()
    hours = UnicodeAttribute()


class LockTable(Model):
    """
    A DynamoDB Lock model
    """

    class Meta(object):
        table_name = os.getenv("DB_LOCK_TABLE_NAME", "dev_lock")
        host = os.getenv("DB_HOST", None)
        region = os.getenv("DB_REGION", "eu-north-1")

    user_id = UnicodeAttribute(hash_key=True)
    event_date = UnicodeAttribute(range_key=True)
