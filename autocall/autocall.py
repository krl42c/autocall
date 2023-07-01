import yaml
import os
import logging
from random import randrange
from typing import List
from autocall import  validator, printer, constants, reporter
from autocall import call as ac
from autocall.reporter import EntryBuilder

CONFIG_TIMEOUT = 300

exceptions = (
    validator.MalformedUrlException,
    validator.UnrecognizedFieldException,
    validator.BadHTTPMethod,
    validator.ExceptedFieldMissing,
    validator.InvalidStatusCode,
    validator.MissingFields
)


def create_calls(config_file) -> dict:
    with open(config_file, encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.UnsafeLoader)
    calls = {}
    for c in config['calls']:
        call : dict = c['call']

        name = call.get('id', str(randrange(0,10000000))) # bug prone?
        # Try to validate current call, if validator throws an exception skip it and continue
        try:
            validator.validate_call(call)
        except exceptions as exception:
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

        calls[name] = ac.Call(name, url, method, expect, headers, query_params, body, timeout, tests, oauth=oauth, dynamic=dynamic)

    return calls


def execute(calls, save_report = False):
    for _,val in calls.items():
        if val.tests is not None:
            val.run_tests()
        else:
            val.execute()
            #entry = EntryBuilder.default(val, 15)
            #print(entry)
