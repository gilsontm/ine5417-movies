
import csv
import base64
from datetime import datetime
from utils.singleton import Singleton
from database.controllers.tweet_controller import TweetController

class Strategy:
    """ Padrão de projeto: Estratégia """
    def export(self, data):
        raise NotImplementedError()

    def get_path(self, extension):
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        return f"file-{date}.{extension}"

class StrategyDocument(Strategy):
    """ Exporta uma análise como documento (.csv) """
    def export(self, data):
        path = self.get_path("csv")
        tweet_controller = TweetController()
        tweets = tweet_controller.get_by_analysis(data["analysis_id"])
        fieldnames = tweets[0].keys() if len(tweets) > 0 else []
        with open(path, "w") as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tweets)
        content_type = "text/csv"
        return path, content_type

class StrategyImage(Strategy):
    """ Exporta uma análise como imagem (.png) """
    def export(self, data):
        path = self.get_path("png")
        header, encoded = data["image"].split(',')
        decoded = base64.b64decode(encoded)
        with open(path, "wb") as pngFile:
            pngFile.write(decoded)
        content_type = "image/png"
        return path, content_type

class Exporter(Singleton):
    """ Classe que exporta uma análise. """
    def __init__(self):
        self.strategy = StrategyDocument()

    def export(self, data):
        return self.strategy.export(data)

    def to_document(self):
        self.strategy = StrategyDocument()

    def to_image(self):
        self.strategy = StrategyImage()
