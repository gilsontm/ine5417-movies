from peewee import IntegerField, TextField
from database import connection

class Entity(connection.BaseModel):
    title = TextField()
    tmdb_id = IntegerField()
    media_type = TextField()

    class Meta:
        table_name = "entity"

def get(entity):
    try:
        return (
            Entity.select()
            .where(Entity.tmdb_id == entity["id"])
            .where(Entity.media_type == entity["media_type"])
            .get()
        )
    except Entity.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def get_or_create(entity):
    return Entity.get_or_create(
        title=entity["title"],
        tmdb_id=entity["id"],
        media_type=entity["media_type"],
    )
