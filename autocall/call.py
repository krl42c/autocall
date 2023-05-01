import requests
import yaml
import json
from typing import List
import os.path
from datetime import datetime
from .import constants, validator, printer

CONFIG_TIMEOUT = 300

class Call:
    def __init__(self, call_id, url, method, expect, headers = None, query_params = None, body = None, timeout = constants.DEFAULT_TIMEOUT, tests = None):
        self.call_id = call_id
        self.url = url
        self.method = method
        self.expect = expect
        self.headers = headers
        self.query_params = query_params
        self.body = body
        self.timeout = timeout
        self.tests = tests

        self.result = None
        self.result_body = None

    def execute(self, 
                print_to_console = True,
                print_response = False,
                save_report = False):
        res : requests.Response = requests.Response()
        try:
            if self.body:
                self.body = json.loads(self.body)
            if self.method == constants.M_GET:
                res = requests.get(self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_POST:
                res = requests.post(self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_PUT:
                res = requests.put(self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)
            elif self.method == constants.M_DELETE:
                res = requests.delete(self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)

            self.result = res.status_code
            self.result_body = res.json()

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

    def save_log(self, target_dir):
        assert self.result
        assert self.result_body
        assert os.path.isdir(target_dir)

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.today().strftime('%Y-%m-%d')

        file_name = f"autocall_log{current_date}-{current_time}"

        with open(target_dir + file_name, 'w+', encoding='utf-8') as file:
            file.write(current_time + '\n')
            file.write(self.url + '\n')
            file.write(self.result + '\n')
            file.write(self.result_body + '\n')

# FIXME: This is horribly bad
def parse_headers(call):
    headers_str : str = "{"
    for key,value in call['headers'].items():
        headers_str += f'"{key}" : "{value}",'
    headers_str = headers_str[:-1]
    headers_str += "}"
    headers = json.loads(headers_str)
    return headers


def create_calls(config_file) -> List[Call]:
    with open(config_file, encoding='utf-8') as file:
        config = yaml.safe_load(file)
    calls = []
    for c in config['calls']:
        call = c['call']
        is_valid = validator.validate_call(call)
        id = call['id']
        url = call['url'] 
        expect = call['expect'] 
        method = call['method']
        timeout = constants.DEFAULT_TIMEOUT

        query_params = None
        body = None
        headers = None
        tests = None

        if 'timeout' in c:
            timeout = c['timeout']
        if 'body' in call:
            body = call['body']
        if 'headers' in call:
            headers = parse_headers(call)
        if 'params' in call:
            query_params = call['params']
        if 'timeout' in call:
            timeout = call['timeout']
        if 'tests' in call:
            tests = call['tests']


        if is_valid:
            calls.append(Call(id, url, method, expect, headers, query_params, body, timeout, tests))
        else:
            print(f'Error validating call inside yaml file: {call}')
    return calls


def execute(calls):
    for c in calls: 
        if c.tests is not None:
            c.run_tests()
        else:
            c.execute()
