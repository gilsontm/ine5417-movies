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
    except Tweet.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def get_overall_sentiment(analysis_id):
    try:
        return (
            Tweet
            .select(fn.SUM(Tweet.sentiment ==  1).alias("positive"),
                    fn.SUM(Tweet.sentiment == -1).alias("negative"))
            .where(Tweet.analysis == analysis_id)
            .get()
        )
    except Tweet.DoesNotExist:
        return None
    except Exception as ex:
        raise ex

def get_coordinates(analysis_id):
    try:
        return (
            Tweet
            .select(Tweet.longitude, Tweet.latitude)
            .where(Tweet.analysis == analysis_id)
            .where(Tweet.longitude.is_null(False))
            .where(Tweet.latitude.is_null(False))
            .execute()
        )
    except Tweet.DoesNotExist:
        return None
    except Exception as ex:
        raise ex