import pytest
import json
from autocall import autocall, constants

OAUTH_SET = "tests/sets/oauth.yaml"


def test_oauth(requests_mock):
    call_set = autocall.create_calls(OAUTH_SET)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2')
    requests_mock.get('http://localhost:8000')
    [val.execute() for key,val in call_set.items()]


OAUTH_NO_HEADERS_SET = "tests/sets/oauth_noheaders.yaml"

def test_oauth_headers(requests_mock):
    call_set = autocall.create_calls(OAUTH_NO_HEADERS_SET)
    response = '{"sdjahdsiuj" : "shadush"}'
    json.loads(response)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2', text=response)
    requests_mock.get('http://localhost:8000', text='token')


    autocall.execute(call_set)
    val = call_set.get('test')
    assert val.headers

