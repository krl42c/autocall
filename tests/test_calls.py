import pytest
import requests
import json
import yaml
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
    with pytest.raises(validator.UnrecognizedFieldException):
        validator.validate_call(load_config_file(UNRECOGNIZED))


def test_excepted_field_missing():
    with pytest.raises(validator.ExceptedFieldMissing):
        validator.validate_call(load_config_file(UNEXCEPTED))


def load_config_file(config):
    with open(config, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)