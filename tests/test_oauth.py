import pytest
from autocall import autocall, constants

OAUTH_SET = "tests/sets/oauth.yaml"


def test_oauth(requests_mock):
    call_set = autocall.create_calls(OAUTH_SET)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2')
    requests_mock.get('http://localhost:8000')
    [val.execute() for key,val in call_set.items()]

