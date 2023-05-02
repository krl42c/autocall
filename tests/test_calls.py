import pytest
import requests
import json
from autocall import call,validator

MULTIPLE_CALLS = "tests/mocks/parametrized.yml"
ALL_METHODS = "tests/mocks/general.yml"
UNRECOGNIZED = "tests/mocks/unrec.yml"
UNEXCEPTED = "tests/mocks/unexcepted.yml"

def test_multiple_calls():
    calls = call.create_calls(MULTIPLE_CALLS)
    try:
        [val.execute() for key,val in calls.items()]
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_all_methods():
    calls = call.create_calls(ALL_METHODS)
    try:
        [val.execute() for key,val in calls.items()]
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_unrecognized_field():
    with pytest.raises(validator.ACUnrecognizedFieldException):
        call.create_calls(UNRECOGNIZED)


def test_excepted_field_missing():
    with pytest.raises(validator.ACExceptedFieldMissing):
        call.create_calls(UNEXCEPTED)
        