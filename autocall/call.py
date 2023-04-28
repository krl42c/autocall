import requests
import yaml
import json
import validate
import printer
from typing import List
import constants

CONFIG_TIMEOUT = 300

class Call:
    def __init__(self, call_id, url, method, expect, headers = None, body = None, timeout = constants.DEFAULT_TIMEOUT, tests = None):
        self.call_id = call_id
        self.url = url
        self.method = method
        self.expect = expect
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.tests = tests

    def execute(self, 
                print_to_console = True,
                print_response = False,
                save_report = False):
        res : requests.Response = requests.Response()
        try:
            if self.body:
                self.body = json.loads(self.body)
            if self.method == constants.M_GET:
                res = requests.get(self.url, headers=self.headers, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_POST:
                res = requests.post(self.url, headers=self.headers, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_PUT:
                res = requests.put(self.url, headers=self.headers, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_DELETE:
                res = requests.delete(self.url, headers=self.headers, json=self.body, timeout=self.timeout)
            if print_to_console:
                printer.print_call(self.expect, self.url, self.call_id, res)
            if print_response:
                print(res.json(), '\n')
        except json.JSONDecodeError:
            print(f'Error parsing request body for {self.url}')
        except requests.RequestException:
            print(f'Error opening connection with host {self.url}')

    def run_tests(self):
        assert self.tests
        for body in self.tests:
            self.body = body['body']
            self.execute()

# FIXME: This is horribly bad
def parse_headers(call):
    headers_str : str = "{"
    for key,value in call['headers'].items():
        headers_str += f'"{key}" : "{value}",'
    headers_str = headers_str[:-1]
    headers_str += "}"
    headers = json.loads(headers_str)
    return headers


def create_calls(config) -> List[Call]:
    calls = []
    for c in config['calls']:
        call = c['call']
        id = call['id']
        url = call['url'] 
        expect = call['expect'] 
        method = call['method']
        timeout = constants.DEFAULT_TIMEOUT

        body = None
        headers = None
        tests = None

        if 'timeout' in c:
            timeout = c['timeout']
        if 'body' in call:
            body = call['body']
        if 'headers' in call:
            headers = parse_headers(call)
        if 'timeout' in call:
            timeout = call['timeout']
        if 'tests' in call:
            tests = call['tests']


        if validate.validate_call(call):
            calls.append(Call(id, url, method, expect, headers, body, timeout, tests))
        else:
            print(f'Error validating call inside yaml file: {call}')
    return calls

