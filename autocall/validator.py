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

keys_with_children = {
    'headers',
    'oauth',
}


# Unitary validation functions`

def validate_call(call : dict):
    def are_keys_valid(call):
        invalid_keys = call.keys() - valid_top_level_keys
        return (False, invalid_keys) if invalid_keys else (True, invalid_keys)
    def are_mandatory_keys_present(call):
        return all(key in call.keys() for key in mandatory_keys)
    def are_headers_valid(headers):
        return isinstance(headers, dict)
    def is_json_valid(body):
        return True if json.loads(body) else False
    def are_tests_valid(node : dict): 
        return all(x.get('body') and is_json_valid(x.get('body')) for x in node)
    def is_http_code_valid(code):
        return True if code in list(HTTPStatus) else False
    def is_method_valid(method):
        return method in constants.METHODS
    def is_url_valid(url):
        return validators.url(url)
    def is_oauth_valid(node : dict):
        return True if node.get('token-url') and node.get('client_id') and node.get('client_secret') else False


    # Check that there are not invalid yaml keys
    keys_valid, keys = are_keys_valid(call)
    if not keys_valid:
        raise UnrecognizedFieldException(keys)
    
    # Check if all needed keys are present
    keys_mandatory = are_mandatory_keys_present(call)
    if not keys_mandatory:
        raise MissingFields(keys)
    
    # Validate HTTP Method
    method = call.get('method') 
    if not is_method_valid(method):
       raise BadHTTPMethod(f"Unrecognized HTTP method {method}")

    status_code = call.get('expect', 200) 
    if not is_http_code_valid(status_code):
        raise InvalidStatusCode(status_code)

    # Check URL 
    if not is_url_valid(call.get('url')):
        raise MalformedUrlException()
    headers = call.get('headers')
    if headers and not are_headers_valid(headers):
        raise Exception('Headers do not contain any values')
    
    if call.get('oauth'):
        if not is_oauth_valid(call.get('oauth')):
            raise ExceptedFieldMissing('Missing fields for OAuth, excepted: ', 'client_id, client_secret, token-url')
    if call.get('tests'):
        if not are_tests_valid(call.get('tests')):
            raise ExceptedFieldMissing('Missing fields for tests, excepted: ', 'call body')

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


class MissingFields(Exception):
    def __init__(self, keys):
        super().__init__(keys)