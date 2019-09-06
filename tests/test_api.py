import requests

local_api = 'http://localhost:8010'
local_db = 'http://localhost:8000'

# sanity check to see that we have some certainty that this test will execute
# on local environment
check_local_db = requests.get(f"{local_db}/shell/")
if check_local_db.status_code != 200:
    raise Exception("Local DB check failed")

check_local_api = requests.get(f"{local_api}/table-names")
if check_local_api.status_code != 200:
    raise Exception("Local API check failed")


def test_create_event():
    data = {
        "reason": "sick",
        "hours": "8",
        "user_name": "Mr User",
        "user_id": "user101",
        "event_date": "2019-03-21"
    }
    r = requests.post(f"{local_api}/events", json=data)
    assert r.status_code == 200


def test_create_lock():
    data = {
        "user_id": "user101",
        "event_date": "2019-03"
    }
    r = requests.post(f"{local_api}/events", json=data)
    assert r.status_code == 200