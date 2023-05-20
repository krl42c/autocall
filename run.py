#!/usr/bin/env python3

import sys
from autocall import autocall

if __name__ == '__main__':
    callset = autocall.create_calls(sys.argv[1])
    autocall.execute(callset)
