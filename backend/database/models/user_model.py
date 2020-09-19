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
        return User.get_by_id(id)
    except User.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def get_by_username(username):
    try:
        return User.select().where(User.username == username).get()
    except User.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def register(user):
    try:
        return User.insert(**user).execute()
    except Exception as ex:
        raise ex