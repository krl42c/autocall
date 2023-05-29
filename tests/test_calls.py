import pytest
import requests
import json
import yaml
from autocall import autocall,validator,constants

MULTIPLE_CALLS = "tests/sets/parametrized.yml"
ALL_METHODS = "tests/sets/general.yml"
UNRECOGNIZED = "tests/sets/unrec.yml"
UNEXCEPTED = "tests/sets/unexcepted.yml"

def test_multiple_calls(requests_mock):
    calls = autocall.create_calls(MULTIPLE_CALLS)

    init_mocks(requests_mock, calls)
    try:
        [val.execute() for key,val in calls.items()]
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_unrecognized_field(requests_mock):
    calls = autocall.create_calls(MULTIPLE_CALLS)

    init_mocks(requests_mock, calls)
    with pytest.raises(validator.UnrecognizedFieldException):
        for c in load_config_file(UNEXCEPTED)['calls']:
            current_call = c['call']
            validator.validate_call(load_config_file(UNRECOGNIZED))


def load_config_file(config):
    with open(config, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    

def init_mocks(requests_mock, calls):
    for call in calls.values():
        if call.method == constants.M_GET:
            requests_mock.get(call.url)
        if call.method == constants.M_POST:
            requests_mock.post(call.url)
        if call.method == constants.M_PUT:
            requests_mock.put(call.url)
        if call.method == constants.M_DELETE:
            requests_mock.delete(call.url)
    