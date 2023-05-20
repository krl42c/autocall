import pytest
from autocall import autocall

OAUTH_SET = "tests/sets/oauth.yaml"


def test_oauth():
    call_set = autocall.create_calls(OAUTH_SET)
    [val.execute() for key,val in call_set.items()]