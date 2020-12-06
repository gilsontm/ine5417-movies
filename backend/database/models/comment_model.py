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

def get_by_entity_id(entity_id):
    try:
        return (Comment.select().where(Comment.entity == entity_id)).execute()
    except Comment.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insert(comment):
    return Comment.insert(**comment).execute()

def remove(comment_id):
    return Comment.delete().where(Comment.id == comment_id).execute()
