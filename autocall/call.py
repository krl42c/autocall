import requests
import yaml
import json
from typing import List
import os.path
from datetime import datetime
from colorama import Fore, Style
from . import constants, validator, printer 

requests_map = {
    constants.M_GET : requests.get,
    constants.M_POST : requests.post,
    constants.M_PUT : requests.put,
    constants.M_DELETE : requests.delete
}

class Call:
    def __init__(self,
                 call_id : str,
                 url : str,
                 method : str,
                 expect : int,
                 headers : dict = None,
                 query_params : dict = None,
                 body : str = None,
                 timeout : int = constants.DEFAULT_TIMEOUT,
                 tests : str = None,
                 oauth : dict = None,
                 dynamic : bool = False):
        self.call_id = call_id
        self.url = url
        self.method = method
        self.expect = expect
        self.headers = headers
        self.query_params = query_params
        self.body = body
        self.timeout = timeout
        self.tests = tests
        self.oauth = oauth
        self.dynamic = dynamic

        self.result = None
        self.result_body = None

    def execute(self, 
                print_to_console = True,
                print_response = False,
                save_report = False, 
                report_target : str = None):
        res : requests.Response = requests.Response()
        try:
            if self.body:
                self.body = json.loads(self.body)

            if self.oauth:
                oauth_token_url = self.oauth.get('token-url')
                oauth_query_params = {
                    'client_id' : self.oauth.get('client_id'),
                    'client_secret' : self.oauth.get('client_secret')
                }
                oauth_res = requests.post(oauth_token_url, params=oauth_query_params, timeout=constants.DEFAULT_TIMEOUT)
                assert oauth_res.json()

                if self.headers is None:
                    self.headers = {'Authorization' : "Bearer" + oauth_res.json()}
                else:
                    self.headers.update({'Authorization' : "Bearer " + (oauth_res.json())})

            print(self.headers)
            res = requests_map[self.method](self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)

            self.result = res.status_code
            self.result_body = res.json()

            if print_to_console:
                printer.print_call(self.expect, self.url, self.call_id, res)
            if print_response:
                print(res.json(), '\n')

            if save_report:
                if report_target:
                    reporter.write_default(report_target, self)

        except json.JSONDecodeError:
            print(f'{Fore.RED}Error parsing request body for {self.url}{Style.RESET_ALL}')
        except requests.RequestException as req_exception:
            print(f'{Fore.RED}Error opening connection with host {self.url}{Style.RESET_ALL}')
            print(req_exception)


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
