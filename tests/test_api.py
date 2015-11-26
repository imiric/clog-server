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
        "INSERT INTO log (hash, data) VALUES ('193fa', 'test')",
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
                'log': {'data': 'test', 'id': 1}
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
    assert data == {
        'id': 1,
        'source': 'post_test',
        'date': '2015-01-01T00:00:00+00:00',
        'log': {'id': 1, 'data': 'post_test'},
    }

    # A second POST with the same log data should reuse the existing log record
    res = client.post('/api/v1/logs/', data=json.dumps(post_data),
                      content_type='application/json')
    assert res.status_code == 201
    data = json.loads(res.data.decode())
    assert data == {
        'id': 2,
        'source': 'post_test',
        'date': '2015-01-01T00:00:00+00:00',
        'log': {'id': 1, 'data': 'post_test'},
    }
