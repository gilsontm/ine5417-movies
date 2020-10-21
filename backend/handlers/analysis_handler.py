import json
import tornado.web
from utils.apis import get_tweepy_api
from database.controllers.entity_controller import EntityController
from database.controllers.analysis_controller import AnalysisController
from database.controllers.tweet_controller import TweetController


class AnalysisHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        pass

    def post(self):
        try:
            request = json.loads(self.request.body)
            entity_controller = EntityController()
            entity = entity_controller.get_or_insert(request["entity"])

            analysis_controller = AnalysisController()
            analysis_id = analysis_controller.insert(request["user_id"], entity["id"])

            tweepy, api = get_tweepy_api()
            try:
                # coletar tweets
                cursor = tweepy.Cursor(api.search, q=request["query"], lang="pt")
                tweets = [tweet for tweet in cursor.items(100)]
            except tweepy.TweepError as ex:
                print(ex)
                self.set_status(401)
            else:
                tweet_controller = TweetController()
                tweet_controller.insert_many(analysis_id, entity["id"], tweets)

                # gerar análises

                self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)
