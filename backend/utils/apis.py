import tweepy
import tmdbsimple

def get_tweepy_api():
    credentials = {}
    credentials['CONSUMER_KEY'] = ""
    credentials['CONSUMER_SECRET'] = ""
    credentials['ACCESS_TOKEN'] = ""
    credentials['ACCESS_SECRET'] = ""
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return tweepy, api

def get_tmdb_api():
    tmdbsimple.API_KEY = ""
    return tmdbsimple
