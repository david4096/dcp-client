# dcp-client

Make it easier to interact with gen3 dcp services.

```
pip install dcp-client
python
$ from dcp.client import Client
$ c = Client()
$ response = c.get(c.indexd_path)
```

Its behavior is meant to be similar to the `requests` module.

