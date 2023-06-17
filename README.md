# Autocall

Automatize network calls using yaml files for testing.

---

## Usage:

```python
from autocall import autocall
call_set = autocall.create_calls('set.yaml')
autocall.execute(call_set)
``````

Example yaml config file:

```yaml

global-timeout: 300
calls:
  - call:
      id : "Base url"
      url : http://localhost:8000
      expect : 200
      headers: 
        userid : '2222'
        authorization : 'Bearer'
      op : GET
      timeout: 500
  - call:
      id : "Get items"
      url : http://localhost:8000/item
      expect : 200
      headers: 
        authorization : 'Bearer *****'
      op : GET
      timeout: 500

```


```yaml

calls:
  - call:
      id: "Send item"
      url: http://localhost:8000/item
      expect: 200
      method: POST
      tests:
        - body: '{
            "name" : "foo",
            "description": "bar",
            "price" : 32 }'
        - body: '{
            "name" : "foo2",
            "description": "bar2",
            "price" : 58 }'

```

---

## Running tests

Regular pytest tests:

```cli
$ TESTS=1 python3 -m pytest tests
```

For testing against a real server there's an Uvicorn server located in tests/test_server and a run.py file in the root directory.

```cli
$ ./run.py /path-to-yaml-file 
```


For debug logs set DEBUG=1 before running.
