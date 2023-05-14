import requests
import yaml
import json
from typing import List
import os.path
from datetime import datetime
from colorama import Fore, Style
from . import constants, validator, printer

CONFIG_TIMEOUT = 300

requests_map = {
    constants.M_GET : requests.get,
    constants.M_POST : requests.post,
    constants.M_PUT : requests.put,
    constants.M_DELETE : requests.delete
}

class Call:
    def __init__(self,
                 call_id,
                 url,
                 method,
                 expect,
                 headers = None,
                 query_params = None,
                 body = None,
                 timeout = constants.DEFAULT_TIMEOUT,
                 tests = None):
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

            res = requests_map[self.method](self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)

            self.result = res.status_code
            self.result_body = res.json()

            if print_to_console:
                printer.print_call(self.expect, self.url, self.call_id, res)
            if print_response:
                print(res.json(), '\n')
        except json.JSONDecodeError:
            print(f'{Fore.RED}Error parsing request body for {self.url}{Style.RESET_ALL}')
        except requests.RequestException:
            print(f'{Fore.RED}Error opening connection with host {self.url}{Style.RESET_ALL}')

    def run_tests(self):
        assert self.tests
        for body in self.tests:
            self.body = body['body']
            self.execute()

    # @TODO: Just a placeholder for now, improve it
    def save_report(self, target_dir):
        assert self.result
        assert self.result_body
        assert os.path.isdir(target_dir)

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.today().strftime('%Y-%m-%d')

        file_name = f"autocall_log{current_date}.txt"

        with open(target_dir + file_name, 'a+', encoding='utf-8') as file:
            file.write(current_time + ': ' + self.url + ' - ' + str(self.result) + '\n')
            file.write(str(self.result_body) + '\n\n\n')


def parse_headers(call):
    return {key: value for key, value in call['headers'].items()}


def create_calls(config_file) -> List[Call]:
    with open(config_file, encoding='utf-8') as file:
        config = yaml.load(file, Loader=yaml.UnsafeLoader)
    calls = {}
    for c in config['calls']:
        call = c['call']

        name = c['id'] if 'id' in c else 'NO ID'

        # Try to validate current call, if validator throws an exception skip it and continue
        try:
            validator.validate_call(call)
        except validator.MalformedUrlException as malformed:
            printer.print_err(name, malformed)
            continue
        except validator.UnrecognizedFieldException as unrec:
            printer.print_err(name, unrec)
            continue
        except validator.BadHTTPMethod as bad_http:
            printer.print_err(name, bad_http)
            continue
        except validator.ExceptedFieldMissing as field_missing:
            printer.print_err(name, field_missing)
            continue
        except validator.InvalidStatusCode as invalid_status:
            printer.print_err(name, invalid_status)
            continue

        url = call['url'] 
        expect = call['expect'] 
        method = call['method']

        query_params = call['params'] if 'params' in call else None
        body = call['body'] if 'body' in call else None
        headers = call['headers'] if 'headers' in call else None
        tests = call['tests'] if 'tests' in call else None
        timeout = call['timeout'] if 'timeout' in call else constants.DEFAULT_TIMEOUT

        calls[id] = Call(name, url, method, expect, headers, query_params, body, timeout, tests)
    return calls


def execute(calls):
    for key,val in calls.items(): 
        if val.tests is not None:
            val.run_tests()
        else:
            val.execute()
