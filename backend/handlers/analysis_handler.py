import json
import tornado.web
import gmaps
from utils.apis import get_tweepy_api
from utils.sentiment.analyser import SentimentAnalyser
from database.controllers.entity_controller import EntityController
from database.controllers.analysis_controller import AnalysisController
from database.controllers.tweet_controller import TweetController
from ipywidgets.embed import embed_minimal_html


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
                tweets = [tweet for tweet in cursor.items(300)]
            except tweepy.TweepError as ex:
                print(ex)
                self.set_status(401)
            else:
                # análise de sentimento
                texts = [tweet.text for tweet in tweets]
                sentiment_analyser = SentimentAnalyser()
                sentiments = sentiment_analyser.analyse(texts)

                for tweet, sentiment in zip(tweets, sentiments):
                    tweet.sentiment = sentiment

                # salvar tweets no banco de dados
                tweet_controller = TweetController()
                tweet_controller.insert_many(analysis_id, entity["id"], tweets)

                # gerar análises
                sentiment = tweet_controller.get_overall_sentiment(analysis_id)

                #heatmap
                heatmap = self.heatmap(tweets)

                self.write({"sentiment" : sentiment, "heatmap": heatmap})
                self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)
            # raise

    def get(self):
        print("/map (GET)")
        if "/map" in self.request.uri:
            with open("export.html") as f:
                self.write(f.read())

    def heatmap(self,tweets):
        gmaps.configure(api_key="AIzaSyBheOZcZc8d7FZ1Ih04WmYlRxa483qA3W8")
        fig = gmaps.figure()
        locations = [tweet.place.bounding_box.origin() for tweet in tweets if tweet.place is not None]
        locations = [(x,y) for y,x in locations]
        fig.add_layer(gmaps.heatmap_layer(locations))
        embed_minimal_html('export.html', views=[fig])
        with open("export.html") as f:
            return f.read()

