import requests

local_api = 'http://localhost:8010'
local_db = 'http://localhost:8000'
testuser = "testuser"
testmonth = "2019-03"
testdate = "2019-03-21"
event_data = {
    "reason": "sick",
    "hours": "8",
    "user_name": "Test Mctest",
    "user_id": f"{testuser}",
    "event_date": f"{testdate}"
}
lock_data = {
    "user_id": f"{testuser}",
    "event_date": f"{testmonth}"
}


# sanity check to see that we have some certainty that this test will execute
# on local environment
check_local_db = requests.get(f"{local_db}/shell/")
if check_local_db.status_code != 200:
    raise Exception("Local DB check failed")

check_local_api = requests.get(f"{local_api}/table-names")
if check_local_api.status_code != 200:
    raise Exception("Local API check failed")


def create_event():
    r = requests.post(f"{local_api}/events", json=event_data)
    return r


def create_lock():
    r = requests.post(f"{local_api}/locks", json=lock_data)
    return r


def test_create_event():
    r = create_event()
    assert r.status_code == 200


def test_create_lock():
    r = create_lock()
    assert r.status_code == 200


def test_list_users():
    r = requests.get(f"{local_api}/users")
    assert r.status_code == 200


def test_get_user():
    create_event()
    r = requests.get(f"{local_api}/users/{testuser}")
    assert r.status_code == 200


def test_list_events_by_user_id():
    create_event()
    r = requests.get(f"{local_api}/users/{testuser}/events")
    assert r.status_code == 200


def test_delete_all_events_by_user_id():
    create_event()
    r = requests.delete(f"{local_api}/users/{testuser}/events")
    assert r.status_code == 200


def test_list_locks_by_user_id():
    create_lock()
    r = requests.get(f"{local_api}/users/{testuser}/locks")
    assert r.status_code == 200


def test_delete_all_locks_by_user_id():
    create_lock()
    r = requests.delete(f"{local_api}/users/{testuser}/locks")
    assert r.status_code == 200


def test_delete_lock_by_user_id_and_date():
    create_lock()
    r = requests.delete(f"{local_api}/users/{testuser}/locks/{testmonth}")
    assert r.status_code == 200


def test_get_event_by_user_id_and_date():
    create_event()
    r = requests.get(f"{local_api}/users/{testuser}/events/")
    assert r.status_code == 200


def test_delete_event_by_user_id_and_date():
    create_event()
    r = requests.delete(f"{local_api}/users/{testuser}/events/{testdate}")
    assert r.status_code == 200


def test_list_all_events():
    create_event()
    r = requests.get(f"{local_api}/events")
    assert r.status_code == 200


def test_list_all_events_by_date():
    create_event()
    r = requests.get(f"{local_api}/events/dates/{testdate}")
    assert r.status_code == 200


def test_delete_all_events_by_date():
    create_event()
    r = requests.delete(f"{local_api}/events/dates/{testdate}")
    assert r.status_code == 200


def test_list_all_locks():
    create_lock()
    r = requests.get(f"{local_api}/locks")
    assert r.status_code == 200


def test_list_all_locks_by_date():
    create_lock()
    r = requests.get(f"{local_api}/locks/dates/{testmonth}")
    assert r.status_code == 200


def test_delete_all_locks_by_date():
    create_lock()
    r = requests.delete(f"{local_api}/locks/dates/{testmonth}")
    assert r.status_code == 200