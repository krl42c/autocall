# Autocall

Automatize network calls using yaml files for testing.

---

## Usage:

```python
from autocall.autocall import SetHandler
callset = SetHandler.from_yaml('path-to-file.yaml')
SetHandler.run_set(callset)
```

Running with thread support enabled (almost always faster):
```cli
$ THREADS=1 ./run.py /path-to-yaml
```

To enable debug prints, set env DEBUG=1, to skip reports while running, set NOOUT=1


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

## Building & Running tests

Build release (generates dist folder and coverage reports inside /build folder)

```cli
$ make release
```

Regular pytest tests:

```cli
$ make test
```

Generate html coverage report:
```cli
$ make coverage
```

For testing against a real server there's an Uvicorn server located in tests/test_server and a run.py file in the root directory.

```cli
$ ./run.py /path-to-yaml-file 
```



For debug logs set DEBUG=1 before running.
