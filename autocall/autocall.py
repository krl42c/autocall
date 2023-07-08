import yaml
import os
import logging
import time
from random import randrange
from typing import List
from autocall import  validator, printer, constants
from autocall.call import Call
from autocall.reporter import EntryBuilder, ReportHelper

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
        call_set_number = 0
        for c in config['calls']:
            call : dict = c['call']
            default_name = f'REQUEST_SET_{call_set_number}'
            name = call.get('id', default_name)

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

            query_params : dict = call.get('params', None)
            body : dict = call.get('body', None)
            headers : dict = call.get('headers', None)
            tests : dict = call.get('tests', None)
            timeout : int = call.get('timeout', constants.DEFAULT_TIMEOUT)
            oauth : dict = call.get('oauth', None)
            dynamic : bool = call.get('dynamic', False)

            calls[name] = Call(name, url, method, expect, headers, query_params, body, timeout, tests, oauth=oauth, dynamic=dynamic)
            call_set_number += 1
        return calls

    @staticmethod
    def from_json(file_path : str):
        # @TODO
        pass
    
    @staticmethod
    def run_set(call_set : dict[str, Call], output : bool = True, html : bool = True):  # call.execute() for each call of the callset
        if os.environ.get('THREADS') == '1':
            from concurrent.futures import ProcessPoolExecutor

            start_time = time.time()
            pool = ProcessPoolExecutor(max_workers=10)
            pool.map(Call.execute, call_set.values())
            end_time = time.time() - start_time
            if os.environ.get('NOOUT')  != '1':
                [print(EntryBuilder.default(call)) for call in call_set.values()]

            if os.environ.get('DEBUG') == '1':
                print(f'All threads ({len(call_set.values())} sets) finished in: {end_time}')
            return


        start_time = time.time()
        for _, call in call_set.items():
            call.execute()
        end_time = time.time() - start_time

        if os.environ.get('NOOUT')  != '1':
            [print(EntryBuilder.default(call)) for call in call_set.values()]
        if os.environ.get('DEBUG') == '1':
            print(f'All calls ({len(call_set.values())} sets) finished in: {end_time}')

        if html:
            html_report = ReportHelper.create_html_report(call_set)
            with open('report.html', 'w') as f:
                f.write(html_report)

    @staticmethod
    def run_set_tests(call_set : dict[str, Call]): 
        for _,call in call_set.items():
            call.run_tests()
