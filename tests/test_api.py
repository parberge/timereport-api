import os
import chalicelib.lib.dynamo_event as dynamo
import requests

local_api = 'http://localhost:8010'
local_db = 'http://localhost:8000'

# sanity check to see that we have some certainty that this test will execute
# on local environment
check_local_db = requests.get(f"{local_db}/shell/")
if check_local_db.status_code != 200:
    raise Exception("Local DB check failed")

check_local_api = requests.get(f"{local_api}/table-name")
if check_local_api.status_code != 200:
    raise Exception("Local API check failed")

def test_get_id(caplog):
    response = requests.get(f"{local_api}/event/users/fake_user")
    assert response is not None
    assert response.text == '[]'
