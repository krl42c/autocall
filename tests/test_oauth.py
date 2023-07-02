import pytest
import json
from autocall.autocall import SetHandler

OAUTH_SET = "tests/sets/oauth.yaml"


def test_oauth(requests_mock):
    call_set = SetHandler.from_yaml(OAUTH_SET)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2')
    requests_mock.get('http://localhost:8000')
    [val.execute() for key,val in call_set.items()]


OAUTH_NO_HEADERS_SET = "tests/sets/oauth_noheaders.yaml"

def test_oauth_headers(requests_mock):
    call_set = SetHandler.from_yaml(OAUTH_NO_HEADERS_SET)
    response = '{"sdjahdsiuj" : "shadush"}'
    json.loads(response)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2', text=response)
    requests_mock.get('http://localhost:8000', text='token')


    SetHandler.run_set(call_set)
    val = call_set.get('test')
    assert val.headers

