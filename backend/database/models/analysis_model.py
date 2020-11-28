from peewee import DateTimeField, ForeignKeyField
from database import connection
from database.models.user_model import User
from database.models.entity_model import Entity
from datetime import datetime


class Analysis(connection.BaseModel):
    created_at = DateTimeField(default=datetime.now)
    user = ForeignKeyField(column_name="user_id", field="id", model=User)
    entity = ForeignKeyField(column_name="entity_id", field="id", model=Entity)

    class Meta:
        table_name = "analysis"

def get_by_user_id(user_id):
    return Analysis.select().where(Analysis.user == user_id).order_by(Analysis.created_at.desc()).execute()

def insert(user_id, entity_id):
    return Analysis.insert(user=user_id, entity=entity_id).execute()
