import pytest
from autocall.call import Call
from autocall.autocall import SetHandler
from autocall.reporter import EntryBuilder, ReportHelper, current_time


def test_default_entry(requests_mock):
    set = SetHandler.from_yaml('tests/sets/ok_all_fields.yaml')

    
    result_call : Call = set.get('All fields / No oauth')

    requests_mock.get(result_call.url)
    requests_mock.post('http://localhost:8000/token?client_id=23238IQsdj&client_secret=ksaudioaud12983u2')

    entry = EntryBuilder.default(result_call, 1)
    excepted_entry = EntryBuilder.format('err', result_call.call_id, result_call.result, result_call.expect, result_call.url, current_time(), 1, ReportHelper.response_time_average(result_call, 1))

    assert entry == excepted_entry


SET = "tests/sets/ok_all_fields.yaml"

def test_html_report():
    target_file = 'test.html'

    call_set = SetHandler.from_yaml(SET)
    html_report = ReportHelper.create_html_report(call_set) 

    assert html_report

    total_calls = len(call_set)
    found_html_li_elements = len([line for line in html_report if line.find('<li>') != -1]) # For every call set there should be a list item in the generated html

    #assert total_calls == found_html_li_elements
   