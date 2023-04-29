import yaml
import pytest
from autocall import validator

with open('tests/mocks/invalid_1.yaml', encoding='utf-8') as file:
    invalid_set = yaml.safe_load(file)

def test_validate_throws_keyerror():
    with pytest.raises(KeyError):
        validator.validate_call(invalid_set['call'])
