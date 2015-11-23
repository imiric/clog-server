import peewee as pw

from config import get_config

CONFIG = get_config()


db = pw.SqliteDatabase(CONFIG.db_path)


class BaseModel(pw.Model):
    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    class Meta:
        database = db
