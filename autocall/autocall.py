from . import  validator, printer, constants, reporter
from . import call as ac
import yaml
import requests
import logging
import os
from typing import List

CONFIG_TIMEOUT = 300

def parse_headers(call):
    return {key: value for key, value in call['headers'].items()}

exceptions = (
    validator.MalformedUrlException,
    validator.UnrecognizedFieldException,
    validator.BadHTTPMethod,
    validator.ExceptedFieldMissing,
    validator.InvalidStatusCode
)

def create_calls(config_file) -> dict:
    with open(config_file, encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.UnsafeLoader)
    calls = {}
    for c in config['calls']:
        call = c['call']

        name = call['id'] if 'id' in call else 'NO ID'

        # Try to validate current call, if validator throws an exception skip it and continue
        try:
            validator.validate_call(call)
        except exceptions as exception:
            printer.print_err(name, exception)
            logging.debug(f"Error validating call set {call}")
            continue

        url = call.get('url')
        expect = call.get('expect')
        method = call.get('method')

        query_params = call.get('params')
        body = call.get('body')
        headers = call.get('headers')
        tests = call.get('tests')
        timeout = call.get('timeout', constants.DEFAULT_TIMEOUT)
        oauth = call.get('oauth')
        dynamic = call.get('dynamic')

        calls[name] = ac.Call(name, url, method, expect, headers, query_params, body, timeout, tests, oauth=oauth, dynamic=dynamic)
        if dynamic:
            parent_id = ddg_find_parent(calls[name])
            if parent_id:
                ddg_construct_body(calls[name], calls[parent_id])
            else:
                continue

    return calls

def ddg_construct_body(child_call : ac.Call, parent_call : ac.Call):
    print("wip")

# @REFACTOR: Hacky mess
def ddg_find_parent(child_call : ac.Call):
    for value in child_call.body.split(" "):
        if value.find("@") != -1:
            ddg = value[value.index("@"):]
            vals = ddg.split(".")
            parent = vals[0][1:] # remove @
            return parent
    return None

def execute(calls, save_report = False):
    for key,val in calls.items(): 
        if val.tests is not None:
            val.run_tests()
        else:
            val.execute()
            if save_report:
                entry = reporter.make_entry(val, True, True, False)
                reporter.write_entry('reports/rep.txt', entry)
