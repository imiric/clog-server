clog-server
===========

Clog is a centralized logging system.

This is the server-side implementation. Clients are available for
[Python](https://github.com/imiric/clog-py) and
[JavaScript](https://github.com/imiric/clog-js).

The server is able to receive logging data via an HTTP JSON API, and display it
on its web dashboard. The logs themselves are stored in a local SQLite database.

If it wasn't obvious so far, this is a toy project and is not meant for
production use at all. Use a proper logging system like Sentry, New Relic, ELK,
etc. instead.


Setup
-----

```
$ git clone https://github.com/imiric/clog-server.git
# Optionally: pyvenv venv && source venv/bin/activate
$ python setup.py develop
```


Usage
-----


0. Create the SQLite DB and schema:
   ```
   $ python -m clog.models.log
   ```

1. Start the server with:
   ```
   python manage.py runserver
   ```
   It will be listening on `localhost:5000`, by default.


To insert some log data, use one of the above-mentioned clients, or simply use
`curl(1)`:

```
$ curl -H 'Content-Type: application/json' \
  -d '{"log": {"data": "Some test exception"}, "source": "my-test-app"}' \
  localhost:5000/api/v1/logs/
```

You should get an HTTP 201 response back with the created log data in the
response body.


Dashboard
---------

The logs can be viewed in the web dashboard, which requires some additional
setup.

1. Install [Node.js w/ npm](https://docs.npmjs.com/getting-started/installing-node).
2. Install frontend dependencies:
   ```
   $ cd clog/web && npm install
   ```
3. Compile frontend assets:
   ```
   $ npm run build
   ```

Finally, load `http://localhost:5000` in your web browser to access the
dashboard.


Configuration
-------------

The configuration is statically defined in `config.py` and can be switched by
setting the `CLOG_ENV` environment variable.

For example:

```
$ CLOG_ENV=prod python manage.py runserver
```

By default, the `dev` configuration is used.


Tests
-----

Install [tox](https://tox.readthedocs.org/en/latest/install.html) and run:

```
$ tox
```


License
-------

[MIT](LICENSE)
