#!/usr/bin/env python3

import sys
from autocall import SetHandler

if __name__ == '__main__':
    callset = SetHandler.from_yaml(sys.argv[1])
    SetHandler.run_set(callset)

