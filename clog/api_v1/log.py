from flask import jsonify, request

from . import api
from ..models import db
from ..models.log import Event, Log
from ..schemas.log import event_schema, events_schema
from ..utils import create_hash


@api.route('/logs/', methods=['GET'])
def get_logs():
    all_events = Event.select()
    result = events_schema.dump(all_events)
    return jsonify(result.data)


@api.route('/logs/', methods=['POST'])
def create_log():
    payload = request.get_json()
    data, errors = event_schema.load(payload)

    if errors:
        return jsonify(errors), 422

    with db.atomic():
        log, created = Log.get_or_create(
            hash=create_hash(data['log']['data']),
            defaults=data['log']
        )
        data['log'] = log

        event = Event.create(**data)

    result = event_schema.dump(event)
    resp = jsonify(result.data)
    resp.status_code = 201
    return resp
