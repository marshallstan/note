from peewee import CharField, ForeignKeyField
from .base_model import BaseModel


class Notebook(BaseModel):
    parent_id = ForeignKeyField('self', null=True, on_delete='cascade', backref='notebooks')
    name = CharField()
    description = CharField(default="")
