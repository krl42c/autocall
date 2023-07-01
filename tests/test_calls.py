import pytest
import yaml
from autocall import autocall, validator

ALL_FIELDS_NO_AUTH = "tests/sets/ok_all_fields_no_auth.yaml"
ALL_FIELDS =  "tests/sets/ok_all_fields.yaml"


UNRECOGNIZED = "tests/sets/ko_unrecognized.yaml"
UNEXCEPTED = "tests/sets/ko_unexcepted.yaml"

def test_all_fields_no_auth(requests_mock):
    calls = autocall.create_calls(ALL_FIELDS_NO_AUTH)
    mock_all(requests_mock, calls)

    try:
        [val.execute() for _, val in calls.items()]
    except Exception:
        pytest.fail("Test failed")


def test_all_fields(requests_mock):
    calls = autocall.create_calls(ALL_FIELDS)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2') # Mock token URL
    mock_all(requests_mock, calls)

    try:
        [val.execute() for _, val in calls.items()]
    except Exception:
        pytest.fail("Test failed")


TESTS =  "tests/sets/ok_tests.yaml"
def test_call_tests(requests_mock):
    calls = autocall.create_calls(TESTS)
    mock_all(requests_mock, calls)
    try:
        [val.execute() for _, val in calls.items()]
    except Exception:
        pytest.fail("Test failed")


# Exceptions
def test_unrecognized(requests_mock):
    with pytest.raises(validator.UnrecognizedFieldException):
        calls = autocall.create_calls(UNRECOGNIZED)
def test_excepted_field_missing(requests_mock):
    with pytest.raises(validator.ExceptedFieldMissing):
        calls = autocall.create_calls(UNEXCEPTED)


def load_config_file(config):
    with open(config, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    

def mock_all(requests_mock, calls):
    for call in calls.values():
        requests_mock.get(call.url)
        requests_mock.post(call.url)
        requests_mock.put(call.url)
        requests_mock.delete(call.url)
    
