import json
import base64
from datetime import datetime
from collections import Counter
from utils.exporter import Exporter
from utils.apis import get_tweepy_api, get_tmdb_api
from handlers.base_handler import BaseHandler
from utils.sentiment.analyser import SentimentAnalyser
from database.controllers.word_controller import WordController
from database.controllers.tweet_controller import TweetController
from database.controllers.entity_controller import EntityController
from database.controllers.analysis_controller import AnalysisController


class AnalysisHandler(BaseHandler):
    def get(self):
        if "/list" in self.request.uri:
            self.get_analysis_list()
        elif "/data" in self.request.uri:
            self.get_analysis_data()

    def get_analysis_list(self):
        try:
            user_id = self.get_argument("user_id", None)
            analysis_controller = AnalysisController()
            analysis = analysis_controller.get_by_user_id(user_id)
            for instance in analysis:
                instance["is_new"] = (datetime.now() - instance["created_at"]).days < 1
                instance["created_at"] = instance["created_at"].strftime("%H:%M %d/%m/%Y")
            self.write({"analysis": analysis})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def get_analysis_data(self):
        try:
            analysis_id = self.get_argument("analysis_id", None)
            tweetController = TweetController()
            sentiment = tweetController.get_overall_sentiment(analysis_id)
            coordinates = tweetController.get_coordinates(analysis_id)
            wordController = WordController()
            words = wordController.get_by_analysis(analysis_id)
            self.write({"sentiment": sentiment, "coordinates": coordinates, "words": words})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def post(self):
        if "/export" in self.request.uri:
            self.export_analysis()
        else:
            self.create_analysis()

    def create_analysis(self):
        try:
            request = json.loads(self.request.body)
            word_controller = WordController()
            tweet_controller = TweetController()
            entity_controller = EntityController()
            analysis_controller = AnalysisController()
            try:
                # coletar tweets
                tweepy, api = get_tweepy_api()
                cursor = tweepy.Cursor(api.search, q=request["query"], lang="pt")
                tweets = [tweet for tweet in cursor.items(100)]
            except tweepy.TweepError as ex:
                print(ex)
                self.set_status(401)
            else:
                # registrar entidade e análise
                entity = entity_controller.get_or_create(request["entity"])
                analysis_id = analysis_controller.insert(request["user_id"], entity["id"])
                # computar análise de sentimento
                texts = [tweet.text for tweet in tweets]
                sentiment_analyser = SentimentAnalyser()
                sentiments, filtered = sentiment_analyser.analyse(texts)
                # salvar tweets no banco de dados
                tweet_controller.insert_many(analysis_id, tweets, sentiments)
                # salvar palavras no banco de dados
                wordcloud = self.create_wordcloud(filtered)
                word_controller.insert_many(analysis_id, wordcloud)
                self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def create_wordcloud(self, filtered):
        counter = Counter()
        for tweet in filtered:
            counter.update(tweet)
        return counter

    def export_analysis(self):
        try:
            request = json.loads(self.request.body)
            exporter = Exporter()
            exporter.to_document()
            if request["format"] == "png":
                exporter.to_image()
            path, content_type = exporter.export(request)
            self.set_header("Content-Type", content_type)
            self.set_header("Content-Disposition", f"attachment; filename={path}")
            self.write(open(path, "rb").read())
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)
