import validators
import json

OPS = ("POST", "GET", "PUT", "DELETE") 

def validate_call(call):
    try:
        url = call['url']
        assert(validators.url(url))

        expect = call['expect']
        assert(int(expect))
        
        op = call['op']
        assert(op in OPS)

        if 'body' in call:
            body = call['body']
            assert(json.loads(body))

    except KeyError:
        print('Unable to parse yaml')
        return False
    return True
