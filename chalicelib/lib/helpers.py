from datetime import timedelta
import logging

log = logging.getLogger("timereport_backend.helpers")


def date_range(start_date, stop_date):
    delta = timedelta(days=1)
    while start_date <= stop_date:
        yield start_date
        start_date += delta


def setup_database(db_engine="dynamodb"):
    log.info(f"DB engine: {repr(db_engine)}")
    if db_engine == "dynamodb":
        from .dynamodb import DynamodbHandler

        return DynamodbHandler()

    if db_engine == "firestore":
        from .firestore import FirestoreHandler

        return FirestoreHandler()
    else:
        raise Exception(f"DB engine {db_engine} not supported")
