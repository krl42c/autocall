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
    'timeout'
)

def validate_call(call):
    for key in call.keys():
        print(key)
        if key not in valid_top_level_keys:
            raise ACUnrecognizedFieldException(f"Unrecognized field {key}")

    url = call['url']
    if not validators.url(url):
        raise ACMalformedUrlException()

    expect = call['expect']

    valid_status = False
    for s in HTTPStatus:
        if expect == s:
            valid_status = True
    
    if not valid_status: 
        raise ACInvalidStatusCode(expect)
    
    op = call['method']
    if op not in constants.METHODS:
        raise ACBadHTTPMethod(f"Unrecognized HTTP method {op}")

    if 'body' in call:
        body = call['body']
        assert json.loads(body)
        
    if 'tests' in call:
        for test in call['tests']:
            if 'body' not in test:
                raise ACExceptedFieldMissing('tests', 'body')
            else:
                assert json.loads(test['body'])

    return True

class ACMalformedUrlException(Exception):
    def __init__(self):
        super().__init__("Malformed URL")

class ACUnrecognizedFieldException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ACBadHTTPMethod(Exception):
    def __init__(self, message):
        super().__init__(message)

class ACExceptedFieldMissing(Exception):
    def __init__(self, parent, excepted):
        message = f"Unexcepted field after {parent}, excepted: {excepted}"
        super().__init__(message)

class ACInvalidStatusCode(Exception):
    def __init__(self, code):
        super().__init__(f'Invalid status code {code}')

