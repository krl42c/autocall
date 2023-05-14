#!/usr/bin/env python3

from autocall import call
import sys

if __name__ == '__main__':
    callset = call.create_calls(sys.argv[1])
    call.execute(callset)
