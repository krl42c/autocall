import pytest
import requests
import json
import yaml
from autocall import autocall,validator

MULTIPLE_CALLS = "tests/sets/parametrized.yml"
ALL_METHODS = "tests/sets/general.yml"
UNRECOGNIZED = "tests/sets/unrec.yml"
UNEXCEPTED = "tests/sets/unexcepted.yml"

def test_multiple_calls():
    calls = autocall.create_calls(MULTIPLE_CALLS)
    try:
        [val.execute() for key,val in calls.items()]
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_all_methods():
    calls = autocall.create_calls(ALL_METHODS)
    try:
        [val.execute() for key,val in calls.items()]
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_unrecognized_field():
    with pytest.raises(validator.UnrecognizedFieldException):
        for c in load_config_file(UNEXCEPTED)['calls']:
            current_call = c['call']
            validator.validate_call(load_config_file(UNRECOGNIZED))


def test_excepted_field_missing():
    with pytest.raises(validator.ExceptedFieldMissing):
        for c in load_config_file(UNEXCEPTED)['calls']:
            current_call = c['call']
            validator.validate_call(current_call)  


def load_config_file(config):
    with open(config, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)