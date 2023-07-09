import os

debug = os.environ.get('DEBUG') == '1'
noout = os.environ.get('NOOUT') == '1'
threads = os.environ.get('THREADS') == '1'
test = os.environ.get('TEST') == '1'