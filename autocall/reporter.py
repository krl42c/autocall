import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import List
from . import call as ac

def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def make_entry(call_rep : ac.Call, 
               log_response = True,
               log_result_code = True,
               log_request_body = True,
               log_time = True,
               log_averages = False,
               number_of_runs = 0
    ) -> str:
    t : str = current_time()
    entry_parts = [t, call_rep.url]

    if log_result_code:
        assert call_rep.result
        entry_parts.append(str(call_rep.result))
    
    if log_response:
        assert call_rep.result_body
        entry_parts.append(str(call_rep.result_body))
        
    if log_request_body:
        assert call_rep.body
        entry_parts.append(str(call_rep.body))

    if log_averages:
        assert call_rep.elapsed
        avg = response_time_average(call_rep, number_of_runs)
        entry_parts.append(str(avg))

    entry = ' '.join(entry_parts)
    return entry


def write_default(target_file : str, call_rep : ac.Call):
    entry = make_entry(call_rep)
    try:
        with open(target_file, 'w+', encoding='utf-8') as file:
            file.write(entry)
    except FileNotFoundError as file_not_found:
        raise file_not_found


def write_entry(target_file : str, entry : str):
    try:
        with open(target_file, 'w+', encoding='utf-8') as file:
            file.write(entry)
    except FileNotFoundError as file_not_found:
        raise file_not_found


def create_html_report(calls : List[ac.Call], target_file : str, water_css = False):
    path = os.path.dirname(os.path.abspath(__file__))

    file_loader = FileSystemLoader(path + '/templates')
    env = Environment(loader=file_loader)

    template = env.get_template('report-blank.html')
    output = template.render(calls=calls, water_css=water_css)

    with open(target_file, 'w', encoding='utf-8') as target:
        target.write(output)


def response_time_average(call : ac.Call, runs_no = 1):
    times : List[float] = []
    for i in range(runs_no):
        call.execute()
        if call.elapsed:
            times.append(call.elapsed.total_seconds())

    return sum(times) / runs_no
