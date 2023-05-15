import json
import validators
from http import HTTPStatus
from . import constants

valid_top_level_keys = (
    'id', 
    'url', 
    'expect', 
    'method',
    'body', 
    'tests', 
    'headers', 
    'timeout',
    'params'
)

def validate_call(call):
    keys = call.keys()
    invalid_keys = keys - valid_top_level_keys
    if invalid_keys:
        raise UnrecognizedFieldException(f"Unrecognized yaml key(s): {', '.join(invalid_keys)}")

    url = call['url']
    if not validators.url(url):
        raise MalformedUrlException()

    expect = call['expect']

    valid_status = False
    for s in HTTPStatus:
        if expect == s:
            valid_status = True
    
    if not valid_status: 
        raise InvalidStatusCode(expect)
    
    op = call['method']
    if op not in constants.METHODS:
        raise BadHTTPMethod(f"Unrecognized HTTP method {op}")

    if 'body' in call:
        body = call['body']
        try:
            json.loads(body)
        except json.JSONDecodeError as bad_json:
            raise bad_json
        
    if 'tests' in call:
        for test in call['tests']:
            if 'body' not in test:
                raise ExceptedFieldMissing('tests', 'body')
            else:
                try:
                    json.loads(test['body'])
                except json.JSONDecodeError as bad_json:
                    raise bad_json

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

