#!/usr/bin/env python3

import sys
from autocall import autocall, reporter

if __name__ == '__main__':
    callset = autocall.create_calls(sys.argv[1])
    autocall.execute(callset, save_report=True)
    reporter.create_html_report(callset.values(), 'my_report.html')

