import json
import validators
import constants

def validate_call(call):
    try:
        url = call['url']
        assert validators.url(url)

        expect = call['expect']
        assert int(expect)
        
        op = call['op']
        assert op in constants.METHODS

        if 'body' in call:
            body = call['body']
            assert json.loads(body)

    except KeyError:
        print('Unable to parse yaml')
        return False
    return True
