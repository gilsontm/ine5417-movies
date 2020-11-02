from peewee import fn, TextField, DoubleField, DateTimeField, ForeignKeyField, IntegerField
from database import connection
from database.models.user_model import User
from database.models.entity_model import Entity
from database.models.analysis_model import Analysis
from datetime import datetime


class Tweet(connection.BaseModel):
    text = TextField(null=False)
    sentiment = IntegerField()
    created_at = DateTimeField(null=False)
    latitude = DoubleField()
    longitude = DoubleField()

    twitter_id = IntegerField()
    author_id = IntegerField()
    author_name = TextField(null=False)
    author_address = TextField(null=False)

    analysis = ForeignKeyField(column_name="analysis_id", field="id", model=Analysis)
    entity = ForeignKeyField(column_name="entity_id", field="id", model=Entity)

    class Meta:
        table_name = "tweet"

def insert_many(tweets):
    try:
        Tweet.insert_many(tweets).execute()
    except Exception as ex:
        raise ex

def get_by_analysis(analysis_id):
    try:
        return Tweet.select().where(Tweet.analysis == analysis_id).execute()
    except Entity.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def get_overall_sentiment(analysis_id):
    try:
        return (
            Tweet
            .select(fn.COUNT(Tweet.id).alias("count"), fn.SUM(Tweet.sentiment).alias("sum"))
            .where(Tweet.analysis == analysis_id)
            .get()
        )
    except Entity.DoesNotExist:
        return None
    except Exception as ex:
        raise ex
