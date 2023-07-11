import os
from datetime import datetime
from colorama import Fore, Style
from jinja2 import Environment, FileSystemLoader
from typing import List
from autocall import call as ac


def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


class ReportHelper:
    @staticmethod
    def response_time_average(call : ac.Call, runs_no = 1):
        times: List[float] = [ call.elapsed.total_seconds() for _ in range(runs_no) if call.execute() and call.elapsed]
        return sum(times) / runs_no
    
    @staticmethod
    def create_html_report(calls : dict[str, ac.Call]):
        path = os.path.dirname(os.path.abspath(__file__))

        # autocall/templates/report-blank.html

        file_loader = FileSystemLoader(path + '/templates')
        env = Environment(loader=file_loader)

        template = env.get_template('report-blank.html') 
        output = template.render(calls=calls.values(), water_css=True)
        return output


class EntryBuilder:
    # Default log example: 
    # .. status test name expected got url timestamp time
    # .. ok - Create new user: <200> <200>      htttp:localhost:980/myapp/create_user   13:43:59   839ms
    # .. ok - Reject new user with wrong data: <400> <400>      htttp:localhost:980/myapp/create_user   13:44:00   200ms
    # .. err - Delete user: <200> <500>      htttp:localhost:980/myapp/delete_user   13:44:01   900ms
    @staticmethod
    def default(call : ac.Call, runs_no : int = 1) -> str:
        result = 'ok' if call.result == call.expect else 'err'
        return EntryBuilder.format(result, call.call_id, call.result, call.expect, call.url, current_time(), runs_no, ReportHelper.response_time_average(call, runs_no))

    @staticmethod
    def err(name: str, exception : Exception):
        return f'{Fore.RED}Error while running set "{name}": {exception}{Style.RESET_ALL}'

    @staticmethod
    def format(result, id, call_result, expect, url, current_time, runs_no, average, cli_colors = True):
        if not cli_colors:
            return f'.. {result} - {id}: <{call_result}> <{expect}>      {url}  {current_time}  Average response time with {runs_no} runs: {average}'
        
        result_color = Fore.GREEN if result == 'ok' else Fore.RED
        return f'..{result_color} {result} {Style.RESET_ALL} - {id}: <{call_result}> <{expect}>      {url}  {current_time}  Average response time with {runs_no} runs: {average}'
    
