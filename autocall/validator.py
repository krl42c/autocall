import json
import validators
from autocall import constants
from http import HTTPStatus


class CallValidator:
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

    @staticmethod
    def are_keys_valid(call : dict) -> bool:
        invalid_keys = call.keys() - CallValidator.valid_top_level_keys
        return (False, invalid_keys) if invalid_keys else (True, invalid_keys)
    @staticmethod
    def are_mandatory_keys_present(call : dict) -> bool:
        return all(key in call.keys() for key in CallValidator.mandatory_keys)
    @staticmethod
    def are_headers_valid(headers) -> bool:
        return isinstance(headers, dict)
    @staticmethod
    def is_json_valid(body) -> bool:
        return True if json.loads(body) else False
    @staticmethod
    def are_tests_valid(node : dict) -> bool: 
        return all(x.get('body') and CallValidator.is_json_valid(x.get('body')) for x in node)
    @staticmethod
    def is_http_code_valid(code : int) -> bool:
        return True if code in list(HTTPStatus) else False
    @staticmethod
    def is_method_valid(method : str) -> bool:
        return method in constants.METHODS
    @staticmethod
    def is_url_valid(url : str) -> bool:
        return validators.url(url)
    @staticmethod
    def is_oauth_valid(node : dict) -> bool:
        return True if node.get('token-url') and node.get('client_id') and node.get('client_secret') else False


def validate_call(call : dict) -> None:

    # Check that there are not invalid yaml keys
    keys_valid, keys = CallValidator.are_keys_valid(call)
    if not keys_valid:
        raise UnrecognizedFieldException(keys)
    
    # Check if all needed keys are present
    keys_mandatory = CallValidator.are_mandatory_keys_present(call)
    if not keys_mandatory:
        raise MissingFields(keys)
    
    # Validate HTTP Method
    method = call.get('method') 
    if not CallValidator.is_method_valid(method):
       raise BadHTTPMethod(f"Unrecognized HTTP method {method}")

    status_code = call.get('expect', 200) 
    if not CallValidator.is_http_code_valid(status_code):
        raise InvalidStatusCode(status_code)

    # Check URL 
    if not CallValidator.is_url_valid(call.get('url')):
        raise MalformedUrlException()
    headers = call.get('headers')
    if headers and not CallValidator.are_headers_valid(headers):
        raise Exception('Headers do not contain any values')
    
    if call.get('oauth'):
        if not CallValidator.is_oauth_valid(call.get('oauth')):
            raise ExceptedFieldMissing('Missing fields for OAuth, excepted: ', 'client_id, client_secret, token-url')
    if call.get('tests'):
        if not CallValidator.are_tests_valid(call.get('tests')):
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