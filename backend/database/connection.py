import sys
import sqlite3
from peewee import SqliteDatabase, Model
from playhouse.shortcuts import model_to_dict


database = SqliteDatabase('./database/database.db')

class BaseModel(Model):
    class Meta:
        database = database

    def as_dict(self, **kwargs):
        return model_to_dict(self, **kwargs)

def setup_database():
    try:
        cursor = sqlite3.connect("./database/database.db")
        cursor.executescript(open("./database/init.sql").read())
        cursor.close()
    except Exception as ex:
        print(ex)
        sys.exit(1)