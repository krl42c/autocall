import yaml
import pytest
import autocall

with open('invalid_1.yaml', encoding='utf-8') as file:
    invalid_set = yaml.safe_load(file)

def test_validate_throws_keyerror():
    with pytest.raises(KeyError):
        autocall.validate_call(invalid_set)