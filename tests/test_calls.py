import pytest
import yaml
import requests
import json
from autocall import call

MULTIPLE_CALLS = "tests/mocks/parametrized.yml"
ALL_METHODS = "tests/mocks/general.yml"

def test_multiple_calls():
    calls = call.create_calls(MULTIPLE_CALLS)
    try:
        for c in calls:
            c.run_tests()
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_all_methods():
    calls = call.create_calls(ALL_METHODS)
    try:
        for c in calls:
            c.execute()
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


