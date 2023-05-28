import pytest
import os
from autocall import autocall, reporter, call

SET = "tests/sets/general.yml"

def test_make_report():
    target_file = 'test.html'

    call_set = autocall.create_calls(SET)
    reporter.create_html_report(call_set, target_file) 

    assert os.path.isfile(target_file)

    content = open(target_file, 'r', encoding='utf-8').readlines()
    assert content

    total_calls = len(call_set)
    found_html_li_elements = len([line for line in content if line.find('<li>') != -1]) # For every call set there should be a list item in the generated html

    assert total_calls == found_html_li_elements
    