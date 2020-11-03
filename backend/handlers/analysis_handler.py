import json
import tornado.web
import gmaps
import base64
import matplotlib.pyplot as plt
from datetime import datetime
from utils.apis import get_tweepy_api
from utils.sentiment.analyser import SentimentAnalyser
from database.controllers.entity_controller import EntityController
from database.controllers.analysis_controller import AnalysisController
from database.controllers.tweet_controller import TweetController
from ipywidgets.embed import embed_minimal_html
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


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
                # análise de sentimento
                texts = [tweet.text for tweet in tweets]
                sentiment_analyser = SentimentAnalyser()
                sentiments = sentiment_analyser.analyse(texts)

                for tweet, sentiment in zip(tweets, sentiments):
                    tweet.sentiment = sentiment

                # salvar tweets no banco de dados
                tweet_controller = TweetController()
                tweet_controller.insert_many(analysis_id, tweets)

                # coletar sentimento
                sentiment = tweet_controller.get_overall_sentiment(analysis_id)
                # gerar heatmap
                heatmap = self.heatmap(tweets)
                # gerar wordcloud
                wordcloud = self.word_cloud(tweets)

                self.write({"sentiment" : sentiment, "heatmap": heatmap, "wordcloud": wordcloud})
                self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def get(self, slug=""):
        if "/heatmap" in self.request.uri:
            with open(slug, "r") as f:
                self.write(f.read())

    def heatmap(self, tweets):
        locations = [tweet.place.bounding_box.origin() for tweet in tweets if tweet.place is not None]
        locations = [(x,y) for y,x in locations]
        if len(locations) > 0:
            gmaps.configure(api_key="AIzaSyBheOZcZc8d7FZ1Ih04WmYlRxa483qA3W8")
            fig = gmaps.figure()
            fig.add_layer(gmaps.heatmap_layer(locations))
            path = f"heatmap-{datetime.strftime(datetime.now(), '%H%M%d%m%Y')}.html"
            embed_minimal_html(path, views=[fig])
            return path
        return ""

    def word_cloud(self, tweets):
        all_tweets_words = " ".join(tweet.text for tweet in tweets)
        stopwords = set(STOPWORDS)
        stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "https"])
        wordcloud = WordCloud(stopwords=stopwords,background_color='white',width=800,height=400).generate(all_tweets_words)
        fig, ax = plt.subplots(figsize=(8,4))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        path = f"wordcloud-{datetime.strftime(datetime.now(), '%H%M%d%m%Y')}.jpg"
        wordcloud.to_file(path)
        with open(path, "rb") as f:
            image = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')
        return image