import requests
import yaml
import json
from typing import List

OP_GET = "GET"
OP_POST = "POST"

class Call:
    def __init__(self, call_id, url, op, expect, headers = None, body = None):
        self.call_id = call_id
        self.url = url
        self.op = op
        self.expect = expect
        self.headers = headers
        if body:
            self.body = json.loads(body)

    def execute(self):
        res = None
        if self.op == OP_GET:
            res = requests.get(self.url)
        if self.op == OP_POST:
            res = requests.post(self.url, json=self.body)
        print(res.json())

with open('config.yml', encoding='utf-8') as f:
    config = yaml.safe_load(f)

calls = []

def create_calls() -> List[Call]:
    for c in config['calls']:
        call = c['call']

        url = call['url'] 
        expect = call['expect'] 
        op = call['op']
        body = None
        headers = None

        if 'body' in call:
            body = call['body']
        if 'headers' in call:
            headers = call['headers']

        calls.append(Call(0, url, op, expect, headers, body))
    return calls

for call in create_calls():
    call.execute()
