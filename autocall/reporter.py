from . import call as ac
from datetime import datetime

whitespace = " "

def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def make_entry(call : ac.Call, 
               log_response = True,
               log_result_code = True,
               log_request_body = True,
               log_time = True,
    ) -> str:
    t : str = current_time()
    entry = ' '.join([t, call.url])

    if log_result_code:
        entry = entry + whitespace + call.result + whitespace
    
    if log_response:
        entry = entry + whitespace + call.result_body + whitespace
   
    if log_request_body:
        entry = entry + whitespace + call.body + whitespace

    if log_time:
        entry = entry + whitespace + t + whitespace
    
    return entry


def write_default(target_file : str, call : ac.Call):
    entry = make_entry(call)
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
