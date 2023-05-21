from datetime import datetime
from . import call as ac

def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def make_entry(call_rep : ac.Call, 
               log_response = True,
               log_result_code = True,
               log_request_body = True,
               log_time = True,
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
