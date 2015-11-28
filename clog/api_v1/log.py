from flask import jsonify, request, abort

from . import api
from ..models import db
from ..models.log import Event, Log
from ..schemas.log import event_schema, events_schema
from ..utils import create_hash


@api.route('/logs/', methods=['GET'])
def get_logs():
    fmt = request.args.get('format')
    ival = request.args.get('interval')
    order_by = request.args.get('order_by')

    data = {}
    if fmt == 'summary' and ival:
        # This query would be convoluted to write with the ORM, and it uses
        # SQLite-specific functions anyway, hence the raw SQL.
        # TODO: Return proper timeslots. The current query returns aggregations
        # with no time gaps between them.
        res = db.execute_sql("""
            -- Aggregate log events into time intervals
            SELECT
                datetime((strftime('%s', date) / ?) * ?, 'unixepoch') interval,
                count(*) cnt
            FROM event
            GROUP BY interval
            ORDER BY interval
        """, (ival, ival)).fetchall()
        data['result'] = dict(res)
    else:
        all_events = Event.select()
        if order_by:
            field = getattr(Event, order_by.lstrip('-'))
            if order_by[0] == '-':
                field = field.desc()
            all_events = all_events.order_by(field)
        data = events_schema.dump(all_events).data

    return jsonify(data)


@api.route('/log/<int:log_id>', methods=['GET'])
def get_log(log_id):
    try:
        evt = Event.get(Event.id == log_id)
    except Event.DoesNotExist:
        abort(404)

    return jsonify(event_schema.dump(evt).data)


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
