from database import connection
from database.models import tweet_model
from peewee import chunked


class TweetController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def insert_many(self, analysis_id, entity_id, tweets):
        parsed_tweets = []
        for tweet in tweets:
            data = {
                "text": tweet.text,
                "created_at": tweet.created_at,
                "latitude": None,
                "longitude": None,
                "twitter_id": tweet.id,
                "author_id": tweet.author.id,
                "author_name": tweet.author.name,
                "author_address": tweet.author.screen_name,
                "analysis": analysis_id,
                "entity": entity_id,
            }
            if tweet.coordinates:
                data["latitude"] = tweet.coordinates.latitude
                data["longitude"] = tweet.coordinates.longitude
            parsed_tweets.append(data)

        with connection.database.atomic() as transaction:
            try:
                for batch in chunked(parsed_tweets, 100):
                    tweet_model.insert_many(batch)
            except KeyboardInterrupt as ex:
                transaction.rollback()
                raise ex
            except Exception as ex:
                transaction.rollback()
                raise ex
