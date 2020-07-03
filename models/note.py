from .base_model import BaseModel
from peewee import CharField, ForeignKeyField
from .notebook import Notebook
import uuid


class Note(BaseModel):
    notebook_id = ForeignKeyField(Notebook, on_delete='cascade', backref='notes')
    uuid = CharField(default=uuid.uuid4)
    title = CharField(default="")
