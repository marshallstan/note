from peewee import Model, DateTimeField, SqliteDatabase
import datetime


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = SqliteDatabase('data/note.db', pragmas={'foreign_keys': 1})

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)
