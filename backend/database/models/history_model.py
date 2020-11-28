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
    return (
        History.select()
        .where(History.user == user_id)
        .order_by(History.id.desc())
        .limit(10)
    )

def remove(user_id, title):
    return (
        History.delete()
        .where(History.user == user_id)
        .where(History.title == title)
        .execute()
    )

def insert(user_id, title):
    already_exists = False
    try:
        history = get(user_id)
        titles = [h.title for h in history]
        if title in titles:
            already_exists = True
    except History.DoesNotExist:
        pass
    if not already_exists:
        return History.insert(user=user_id, title=title).execute()
