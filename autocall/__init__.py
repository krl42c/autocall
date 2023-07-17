import os
import logging

from autocall.autocall import SetHandler

if not os.path.exists('logs'):
    os.mkdir('logs')

dbg = os.environ.get('DEBUG') == '1'
logging.basicConfig(filename='logs/autocall.log', level=logging.DEBUG if dbg else logging.INFO)



if __name__ == '__main__':
    print('yikes')