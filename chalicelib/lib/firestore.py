import logging
import os
from google.cloud import firestore

log = logging.getLogger(f"timereport_backend.{__name__}")


class FirestoreHandler:
    def __init__(self):
        self.events = os.getenv("DB_EVENT_TABLE_NAME", "dev_event")
        self.locks = os.getenv("DB_LOCK_TABLE_NAME", "dev_lock")
        self.db = firestore.Client(project="timereport")

    def get_tables(self):
        return "Not applicable for firestore"

    def list_users(self):
        """
        returns list of all users
        """
        raise Exception("Not implemented yet")

    def get_user(self, user_id):
        """
        returns user_id or empty
        """
        raise Exception("Not implemented yet")

    def list_events_by_user_id(self, user_id, date_from=None, date_to=None):
        """
        :param user_id:
        :param date_from: optional
        :param date_to: optional
        :return: list of events for user_id
        """
        raise Exception("Not implemented yet")

    def delete_all_events_by_user_id(self, user_id):
        """
        :param user_id:
        :return: status
        """
        raise Exception("Not implemented yet")

    def get_event_by_user_id_and_date(self, user_id, event_date):
        """
        :param user_id:
        :param event_date:
        :return: event
        """
        raise Exception("Not implemented yet")

    def delete_event_by_user_id_and_date(self, user_id, event_date):
        """
        :param user_id:
        :param event_date:
        :return: method, user_id, count, status
        """
        raise Exception("Not implemented yet")

    def list_locks_by_user_id(self, user_id):
        """
        :param user_id:
        :return: list of locks for user
        """
        raise Exception("Not implemented yet")

    def delete_all_locks_by_user_id(self, user_id):
        """
        :param user_id:
        :return: method, user_id, count, status
        """
        raise Exception("Not implemented yet")

    def get_lock_by_user_id_and_date(self, user_id, event_date):
        """
        :param user_id:
        :param event_date:
        :return: lock for user
        """
        raise Exception("Not implemented yet")

    def delete_lock_by_user_id_and_date(self, user_id, event_date):
        """
        :param user_id:
        :param event_date:
        :return: status
        """
        raise Exception("Not implemented yet")

    def list_all_events(self):
        """
        :return: list of all events
        """
        raise Exception("Not implemented yet")

    def list_all_events_by_date(self, event_date):
        """
        :param event_date:
        :return: list of all events for date
        """
        raise Exception("Not implemented yet")

    def create_event_v2(self, events):
        """
        :param events:
        :return: status
        """
        # document = self.db.collection(collection).document()
        raise Exception("Not implemented yet")

    def delete_all_events_by_date(self, event_date):
        """
        :param event_date:
        :return: status
        """
        raise Exception("Not implemented yet")

    def list_all_locks(self):
        """
        :return: list of all locks
        """
        lock_documents = self.db.collection(self.locks)
        lock_stream = lock_documents.stream()
        locks = [doc.to_dict() for doc in lock_stream]
        return json.dumps(locks)

    def create_lock(self, lock_request):
        """
        :param lock_request:
        :return: status
        """
        log.info(f"Lock request: {lock_request}")
        lock_event = self.db.collection(self.locks).document(
            lock_request.get(self.locks)
        )
        return str(
            lock_event.set(
                {
                    "user_id": lock_request.get("user_id"),
                    "event_date": lock_request.get("event_date"),
                }
            )
        )

    def list_all_locks_by_date(self, event_date):
        """
        :param event_date:
        :return: list of locks for date
        """
        raise Exception("Not implemented yet")

    def delete_all_locks_by_date(self, event_date):
        """
        :param event_date:
        :return: status
        """
        raise Exception("Not implemented yet")
