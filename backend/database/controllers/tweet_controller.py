from database import connection
from database.models import tweet_model


class TweetController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def insert_many(self, analysis_id, tweets, sentiments):
        parsed_tweets = []
        for tweet, sentiment in zip(tweets, sentiments):
            data = {
                "text": tweet.text,
                "sentiment": sentiment,
                "created_at": tweet.created_at,
                "latitude": None,
                "longitude": None,
                "twitter_id": tweet.id,
                "author_id": tweet.author.id,
                "author_name": tweet.author.name,
                "author_address": tweet.author.screen_name,
                "analysis": analysis_id,
            }
            if tweet.place:
                origin = tweet.place.bounding_box.origin()
                data["latitude"] = origin[1]
                data["longitude"] = origin[0]
            parsed_tweets.append(data)
        tweet_model.insert_many(parsed_tweets)

    def get_by_analysis(self, analysis_id):
        tweets = tweet_model.get_by_analysis(analysis_id)
        if tweets is None:
            return []
        results = [tweet.as_dict(recurse=False) for tweet in tweets]
        return results

    def get_overall_sentiment(self, analysis_id):
        sentiment = tweet_model.get_overall_sentiment(analysis_id)
        if sentiment is None:
            return None
        positive = sentiment.positive * 100 / (sentiment.positive + sentiment.negative)
        return positive

    def get_coordinates(self, analysis_id):
        coordinates = tweet_model.get_coordinates(analysis_id)
        if coordinates is None:
            return []
        coordinates = [[tweet.latitude, tweet.longitude] for tweet in coordinates]
        return coordinates
