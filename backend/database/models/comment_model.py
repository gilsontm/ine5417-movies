from datetime import datetime
from peewee import TextField, DateTimeField, ForeignKeyField
from database import connection
from database.models.user_model import User
from database.models.entity_model import Entity

class Comment(connection.BaseModel):
    text = TextField()
    created_at = DateTimeField(default=datetime.now)
    user = ForeignKeyField(column_name="user_id", field="id", model=User)
    entity = ForeignKeyField(column_name="entity_id", field="id", model=Entity)

    class Meta:
        table_name = "comment"

def get_by_tmdb_id(tmdb_id):
    try:
        return (
            Comment.select()
            .join(Entity, on=(Entity.id == Comment.entity_id))
            .where(Entity.tmdb_id == tmdb_id)
            .order_by(Comment.created_at.desc())
        ).execute()
    except Comment.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insert(text, user_id, entity_id):
    return Comment.insert(text=text, user_id=user_id, entity_id=entity_id).execute()
