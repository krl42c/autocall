import pytest
import os
from autocall.reporter import ReportHelper
from autocall.autocall import SetHandler

SET = "tests/sets/ok_all_fields.yaml"

def test_make_report():
    target_file = 'test.html'

    call_set = SetHandler.from_yaml(SET)
    html_report = ReportHelper.create_html_report(call_set) 

    assert html_report

    total_calls = len(call_set)
    found_html_li_elements = len([line for line in html_report if line.find('<li>') != -1]) # For every call set there should be a list item in the generated html

    #assert total_calls == found_html_li_elements
   