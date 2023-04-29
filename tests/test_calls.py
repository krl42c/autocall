import pytest
import yaml
import requests
import json
from autocall import call

with open("tests/mocks/parametrized.yml", encoding="utf-8") as file:
    multiple_calls = yaml.safe_load(file)

with open("tests/mocks/general.yml", encoding="utf-8") as file:
    general = yaml.safe_load(file)


def test_multiple_calls():
    calls = call.create_calls(multiple_calls)
    try:
        for c in calls:
            c.run_tests()
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


def test_all_methods():
    calls = call.create_calls(general)
    try:
        for c in calls:
            c.execute()
    except requests.RequestException:
        pytest.fail("Request failed")
    except json.JSONDecodeError:
        pytest.fail("JSON decode failed")


