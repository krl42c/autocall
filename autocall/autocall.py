import yaml
import os
import logging
from random import randrange
from typing import List
from autocall import  validator, printer, constants
from autocall.call import Call
from autocall.reporter import EntryBuilder

class SetHandler:
    exception_map = (
        validator.MalformedUrlException,
        validator.UnrecognizedFieldException,
        validator.BadHTTPMethod,
        validator.ExceptedFieldMissing,
        validator.InvalidStatusCode,
        validator.MissingFields
    )

    @staticmethod
    def from_yaml(file_path : str) -> dict[str, Call]:
        with open(file_path, encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.UnsafeLoader)
        calls = {}
        for c in config['calls']:
            call : dict = c['call']

            name = call.get('id', str(randrange(0,10000000))) # bug prone?
        # Try to validate current call, if validator throws an exception skip it and continue
            try:
                validator.validate_call(call)
            except SetHandler.exception_map as exception:
                printer.print_err(name, exception)
                logging.debug("Error validating call set %s", call)
                if os.environ.get('TEST') == '1':
                    raise exception 
                continue

            url = call.get('url')
            expect = call.get('expect', 200)
            method = call.get('method')

            query_params = call.get('params')
            body = call.get('body')
            headers = call.get('headers')
            tests = call.get('tests')
            timeout = call.get('timeout', constants.DEFAULT_TIMEOUT)
            oauth = call.get('oauth')
            dynamic = call.get('dynamic')

            calls[name] = Call(name, url, method, expect, headers, query_params, body, timeout, tests, oauth=oauth, dynamic=dynamic)

        return calls

    @staticmethod
    def from_json(file_path : str):
        # @TODO
        pass
    
    @staticmethod
    def run_set(call_set : dict[str, Call]):
        for _, call in call_set.items():
            call.execute()

    @staticmethod
    def run_set_tests(call_set : dict[str, Call]):
        for _,call in call_set.items():
            call.run_tests()