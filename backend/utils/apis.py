import tweepy
import tmdbsimple

def get_tweepy_api():
    credentials = {}
    credentials['CONSUMER_KEY'] = "E5UX7wTaZwt4zhZxvHc0WNHOR"
    credentials['CONSUMER_SECRET'] = "4xw8KumzcSoR35nrZZI3sI0qLzz3yhtqbdvnZf4YMURavJmXnd"
    credentials['ACCESS_TOKEN'] = "1279538135601381376-KdQXyasrpYZ4IlzNLPQrQOn7DRDshW"
    credentials['ACCESS_SECRET'] = "Mxi7sIoQ0dp1pQYzn9ze4hkHHkM1imDOPjgj9kDg4qpjB"
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return tweepy, api

def get_tmdb_api():
    tmdbsimple.API_KEY = "a7be76f64e55cd2dce20c2db9fb333cd"
    return tmdbsimple
