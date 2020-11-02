import json
import tornado.web
from datetime import datetime
from utils.apis import get_tmdb_api
from utils.apis import get_tweepy_api
from database.controllers.favorite_controller import FavoriteController
from database.controllers.search_history_controller import HistoryController

class SearchHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        pass

    def get(self):
        if "/search" in self.request.uri:
            self.search()
        elif "/info" in self.request.uri:
            self.info()
        elif "/history" in self.request.uri:
            self.history()

    def history(self):
        try:
            user_id = self.get_argument("user_id", None)

            history_controller = HistoryController()
            self.write({"results": history_controller.get(user_id)})

        except Exception as ex:
            print(ex)
            self.set_status(500)
            raise

    def search(self):
        try:
            query = self.get_argument("query", None)
            user_id = self.get_argument("user_id", None)

            history_controller = HistoryController()
            history_controller.insert(user_id,query)

            search = get_tmdb_api().Search()
            promise = search.multi(query=query, language="pt")
            results = [result for result in search.results]
            self.write({"results": results})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)
            raise

    def info(self):
        try:
            api = get_tmdb_api()
            user_id = self.get_argument("user_id", None)
            entity = json.loads(self.get_argument("entity", None))

            favorite_controller = FavoriteController()
            is_favorite = favorite_controller.is_favorite(user_id, entity)

            if entity["media_type"] == "movie":
                model = api.Movies(entity["id"])
                related = model.similar_movies(language="pt")["results"]
            elif entity["media_type"] == "tv":
                model = api.TV(entity["id"])
                related = model.similar(language="pt")["results"]
            else:
                model = api.People(entity["id"])
                response = model.combined_credits(language="pt")
                related = response["cast"] + response["crew"]

            query = self.get_argument("query", None)
            tweets = self.get_recent_tweets(query)

            self.write({
                "info": model.info(language="pt"),
                "related": related,
                "is_favorite": is_favorite,
                "recent_tweets": tweets,
            })
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def get_recent_tweets(self, query):
        tweepy, api = get_tweepy_api()
        try:
            cursor = tweepy.Cursor(api.search, q=query, lang="pt")
            tweets = [tweet for tweet in cursor.items(15)]
        except tweepy.TweepError as ex:
            tweets = []
        tweets = [
            {
                "id": tweet.id,
                "text": tweet.text,
                "author_name": tweet.author.name,
                "author_address": tweet.author.screen_name,
                "created_at": datetime.strftime(tweet.created_at, "%H:%M %d/%m/%Y")
            } for tweet in tweets
        ]
        return tweets
