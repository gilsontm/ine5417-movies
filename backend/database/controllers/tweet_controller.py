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
                "sentiment": tweet.sentiment,
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
            # if tweet.coordinates:
            #     data["latitude"] = tweet.coordinates.latitude
            #     data["longitude"] = tweet.coordinates.longitude
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

    def get_by_analysis(self, analysis_id):
        tweets = tweet_model.get_by_analysis(analysis_id)
        if tweets is None:
            return []
        results = [tweet.as_dict() for tweet in tweets]
        return results

    def get_overall_sentiment(self, analysis_id):
        sentiment = tweet_model.get_overall_sentiment(analysis_id)
        if sentiment is None:
            return None
        positive = (sentiment.count - abs(sentiment.sum)) / 2
        if sentiment.sum > 0:
            positive += sentiment.sum
        percentage = positive / (sentiment.count) * 100
        return percentage