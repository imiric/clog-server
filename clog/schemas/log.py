from ..app import ma
from ..models.log import Log

from marshmallow import post_dump, fields


class BaseSchema(ma.Schema):
    @post_dump(pass_many=True)
    def wrap(self, data, many):
        if many:
            data = {'results': data, 'count': len(data)}
        return data


class LogSchema(BaseSchema):
    data = fields.Str(required=True)

    class Meta:
        fields = ('id', 'data')


class EventSchema(BaseSchema):
    source = fields.Str(required=True)
    log = fields.Nested(LogSchema, required=True)

    class Meta:
        fields = ('id', 'source', 'date', 'log')


log_schema = LogSchema()
logs_schema = LogSchema(many=True)

event_schema = EventSchema()
events_schema = EventSchema(many=True)
