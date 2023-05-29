import json
import validators
from autocall import constants
from http import HTTPStatus

valid_top_level_keys = (
    'id', 
    'url', 
    'expect', 
    'method',
    'body', 
    'tests', 
    'headers', 
    'timeout',
    'params',
    'oauth',
    'dynamic'
)

mandatory_keys = {
    'url',
    'method'
}

def are_mandatory_keys_present(call):
    for key in mandatory_keys:
        if key not in call.keys():
            return False
    return True


# Multiple return in order to enable exception message to include invalid keys
# kinda ugly
def are_keys_valid(call):
    keys = call.keys()
    invalid_keys = keys - valid_top_level_keys
    if invalid_keys:
        return False, invalid_keys
    else:
        return True, invalid_keys
    

def is_http_code_valid(code):
    for http_code in HTTPStatus:
        if code == http_code:
            return True
    return False


def is_method_valid(method):
    return method in constants.METHODS


def is_json_valid(body):
    try:
        json.loads(body)
        return True
    except json.JSONDecodeError:
        return False


def is_url_valid(url):
    return validators.url(url)


def validate_call(call):
    # Check that there are not invalid yaml keys
    keys_valid, keys = are_keys_valid(call)
    if not keys_valid:
        raise UnrecognizedFieldException(keys)
    
    # Check if all needed keys are present
    keys_mandatory = are_mandatory_keys_present(call)
    if not keys_mandatory:
        raise UnrecognizedFieldException(keys)
    
    # Validate HTTP Method
    method = call.get('method') 
    if not is_method_valid(method):
       raise BadHTTPMethod(f"Unrecognized HTTP method {method}")

    status_code = call.get('expect') 
    if not is_http_code_valid(status_code):
        raise InvalidStatusCode(status_code)

    # Check URL 
    if not is_url_valid(call.get('url')):
        raise MalformedUrlException()


class MalformedUrlException(Exception):
    def __init__(self):
        super().__init__("Malformed URL")

class UnrecognizedFieldException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadHTTPMethod(Exception):
    def __init__(self, message):
        super().__init__(message)

class ExceptedFieldMissing(Exception):
    def __init__(self, parent, excepted):
        message = f"Unexcepted field after {parent}, excepted: {excepted}"
        super().__init__(message)

class InvalidStatusCode(Exception):
    def __init__(self, code):
        super().__init__(f'Invalid status code {code}')