import json
from datetime import datetime

import pytest


@pytest.fixture
def create_schema():
    from clog.models.log import create_tables
    create_tables()


@pytest.fixture
def create_log_data(create_schema):
    from clog.models import db
    sql = [
        "INSERT INTO log (hash, data, metadata) "
        "VALUES ('193fa', 'test', '{}')",
        "INSERT INTO event (log_id, source, date) "
        "VALUES (1, 'test', '2015-01-01')",
    ]
    list(map(db.execute_sql, sql))


@pytest.fixture
def client():
    from clog.app import create_app
    return create_app().test_client()


@pytest.fixture
def patch_date(monkeypatch):
    monkeypatch.setattr('clog.api_v1.log.Event._meta._default_callable_list',
                        [('date', lambda: datetime(2015, 1, 1))])


@pytest.mark.usefixtures('create_log_data')
def test_get_logs(client):
    res = client.get('/api/v1/logs/')
    assert res.status_code == 200
    data = json.loads(res.data.decode())
    assert data == {
        'count': 1,
        'result': [
            {
                'id': 1,
                'source': 'test',
                'date': '2015-01-01T00:00:00+00:00',
                'log': {'data': 'test', 'id': 1, 'hash': '193fa',
                        'metadata': '{}'}
            }
        ]
    }


@pytest.mark.usefixtures('create_schema', 'patch_date')
def test_post_logs(client):
    post_data = {
        'source': 'post_test',
        'log': {
            'data': 'post_test'
        }
    }
    res = client.post('/api/v1/logs/', data=json.dumps(post_data),
                      content_type='application/json')
    assert res.status_code == 201
    data = json.loads(res.data.decode())

    expected_log = {
        'id': 1, 'data': 'post_test', 'metadata': '{}',
        'hash': ('81ab1411a3a07804d4c1484e971bb9aa'
                 '866d41ef66da89df40b4a1483c58141a')
    }
    assert data == {
        'id': 1,
        'source': 'post_test',
        'date': '2015-01-01T00:00:00+00:00',
        'log': expected_log
    }

    # A second POST with the same log data should create a new event, but reuse
    # the existing log record.
    res = client.post('/api/v1/logs/', data=json.dumps(post_data),
                      content_type='application/json')
    assert res.status_code == 201
    data = json.loads(res.data.decode())
    assert data == {
        'id': 2,
        'source': 'post_test',
        'date': '2015-01-01T00:00:00+00:00',
        'log': expected_log
    }


@pytest.mark.usefixtures('create_schema')
def test_rate_limit(client):
    res = None

    for i in range(10):
        res = client.post('/api/v1/logs/',
                          data='{"log": {"data": "test"}, "source": "me"}',
                          content_type='application/json')
        if res.status_code == 429:
            break

    assert json.loads(res.data.decode()) == {
        'error': 'exceeded ratelimit of 5 per 1 minute'
    }
