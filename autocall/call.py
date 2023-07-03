import requests
import yaml
import json
from typing import List
import os.path
import logging
from datetime import datetime
from colorama import Fore, Style
from autocall import constants, printer


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
                 dynamic : bool = False,
                 ):
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
        self.elapsed = None
        self.success = False

    def execute(self, 
                print_to_console = True,
                print_response = False,
                ):
        res : requests.Response = requests.Response()
        logging.debug("[%s] Running request", self.url)
        try:
            if self.body:
                if isinstance(self.body, dict): 
                    self.body = json.dumps(self.body)
                else:
                    self.body = json.loads(self.body)

            if self.oauth:
                logging.debug("[%s][OAUTH] Running oauth token request", self.url)
                oauth_token_url = self.oauth.get('token-url')
                oauth_query_params = {
                    'client_id' : self.oauth.get('client_id'),
                    'client_secret' : self.oauth.get('client_secret')
                }
                oauth_res = requests.post(oauth_token_url, params=oauth_query_params, timeout=constants.DEFAULT_TIMEOUT)
                
                if self.headers is None:
                    self.headers = {'Authorization' : "Bearer " + str(oauth_res.json())}
                else:
                    self.headers.update({'Authorization' : "Bearer " + str((oauth_res.json()))})

            res = requests_map[self.method](self.url, headers=self.headers, params=self.query_params, json=self.body, timeout=self.timeout)

            self.result = res.status_code
            self.result_body = res.json()
            self.elapsed = res.elapsed

            #if print_to_console:
            #    printer.print_call(self.expect, self.url, self.call_id, res)
            #    pass
            #if print_response:
            #    print(res.json(), '\n')

            self.success = True

        except json.JSONDecodeError as json_decode_error:
            print(f'{Fore.RED}Error parsing request body for {self.url}{Style.RESET_ALL}')
            logging.debug("[{%s}][ERROR]: error executing request, problem with json body: {%s}", self.url, json_decode_error.msg)

        except requests.RequestException as req_exception:
            print(f'{Fore.RED}Error opening connection with host {self.url}{Style.RESET_ALL}')
            logging.debug("[%s][ERROR]: error executing request: %s", self.url, req_exception)
            print(req_exception)


    def run_tests(self):
        assert self.tests
        for body in self.tests:
            self.body = body['body']
            self.execute()