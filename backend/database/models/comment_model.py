from datetime import datetime
from peewee import TextField, DateTimeField, ForeignKeyField, JOIN
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

def get_by_entity_id(tmdb_id):
    """
        select User.username, Comment.text, Comment.created_at
        from Comment
        left out join User on User.id == Comment.user_id
    """
    try:
        return (Comment.select(Comment.text, Comment.created_at)
                       .join(Entity)
                       .dicts()
                    #    .where(Entity.tmdb_id == tmdb_id)
                )
    except Comment.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insert(comment,user_id,entity_id):
    return Comment.insert(text=comment,user_id=user_id,entity_id=entity_id).execute()

def remove(comment_id):
    return Comment.delete().where(Comment.id == comment_id).execute()
