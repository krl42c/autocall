# Autocall

Automatize network calls using yaml files for testing.

Usage:

```cli
    $ python3 autocall.py call_set.yaml
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

Output:

![](docs/output.png)