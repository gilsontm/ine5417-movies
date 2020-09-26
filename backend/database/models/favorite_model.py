from peewee import ForeignKeyField
from database import connection
from database.models.user_model import User
from database.models.entity_model import Entity

class Favorite(connection.BaseModel):
    user = ForeignKeyField(column_name="user_id", field="id", model=User)
    entity = ForeignKeyField(column_name="entity_id", field="id", model=Entity)

    class Meta:
        table_name = "favorite"

def get(user_id, entity_id):
    try:
        return (
            Favorite.select()
            .where(Favorite.user == user_id)
            .where(Favorite.entity == entity_id)
            .get()
        )
    except Favorite.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def insert(user_id, entity_id):
    return Favorite.insert(user=user_id, entity=entity_id).execute()

def remove(user_id, entity_id):
    return (
        Favorite.delete()
        .where(Favorite.user == user_id)
        .where(Favorite.entity == entity_id)
        .execute()
    )

def get_by_user_id(user_id):
    try:
        return Favorite.select().where(Favorite.user == user_id)
    except Favorite.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
