from peewee import ForeignKeyField
from peewee import TextField
from database import connection
from database.models.user_model import User

class History(connection.BaseModel):
    user = ForeignKeyField(column_name="user_id", field="id", model=User)
    title = TextField()

    class Meta:
        table_name = "history"

def get(user_id):
    try:
        return (
            History.select()
            .where(History.user == user_id)
            .limit(10)
            .get()
        )
    except History.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def remove(user_id, title):
    return (
        History.delete()
        .where(History.user == user_id)
        .where(History.title == title)
        .execute()
    )

def insert(user_id, title):
    return History.insert(user=user_id, title=title).execute()