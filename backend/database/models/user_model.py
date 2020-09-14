from peewee import TextField
from database import connection


class User(connection.BaseModel):
    name = TextField()
    email = TextField()
    username = TextField()
    password = TextField()

    class Meta:
        table_name = "user"

def get_by_id(id):
    try:
        return User.select().where(User.id == id).get()
    except User.DoesNotExist:
        return None
    except Exception as ex:
        raise ex