from datetime import datetime

import peewee as pw

from . import db, BaseModel


class Log(BaseModel):
    hash = pw.CharField(max_length=255)
    data = pw.TextField()


class Event(BaseModel):
    log = pw.ForeignKeyField(Log, related_name='events')
    source = pw.CharField(max_length=255)
    date = pw.DateTimeField(default=datetime.now)


def create_tables():
    db.connect()
    db.create_tables([Log, Event])


if __name__ == '__main__':
    create_tables()
