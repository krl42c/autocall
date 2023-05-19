# Autocall

Automatize network calls using yaml files for testing.

---

## Usage:

```python
from autocall import call
call_set = call.create_calls('set.yaml')
call.execute(call_set)
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

Run the run_tests.sh script, an Uvicorn server located in tests/test_server will launch and the pytest suite will be ran against it.

```cli
$ pip3 install -r requirements.txt
$ ./run_tests.sh
```
