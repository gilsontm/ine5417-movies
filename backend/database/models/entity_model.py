from peewee import IntegerField, TextField
from database import connection

class Entity(connection.BaseModel):
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

def insert(entity):
    return Entity.create(
            tmdb_id=entity["id"],
            media_type=entity["media_type"]
        )
