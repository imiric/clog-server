import os

import peewee as pw

from config import basedir


db = pw.SqliteDatabase(os.path.join(basedir, 'clog.db'))


class BaseModel(pw.Model):
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    class Meta:
        database = db
