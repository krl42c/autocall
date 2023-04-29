import yaml
import pytest
from autocall import validator

with open('tests/mocks/invalid_1.yaml', encoding='utf-8') as file:
    invalid_set = yaml.safe_load(file)

with open('tests/mocks/parametrized.yml', encoding='utf-8') as file:
    valid_set = yaml.safe_load(file)


def test_validate_throws_keyerror():
    with pytest.raises(KeyError):
        validator.validate_call(invalid_set['call'])

def test_parametrized():
    try: 
        validator.validate_call(valid_set)
    except KeyError:
        pytest.fail("Validator failed to valid yaml parametrized.yml")
    except IndexError:
        pytest.fail("Validator failed to valid yaml parametrized.yml")