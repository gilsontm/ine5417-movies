import os
import random
import pickle
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier
from utils.sentiment.cleaner import Cleaner

class SentimentAnalyser:
    """ Singleton """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.cleaner = Cleaner()
        self.loaded = False
        if os.path.exists(self.get_model_path()):
            self.load_classifier()

    def get_model_path(self):
        return f"{os.path.dirname(__file__)}/models/analyser.pkl"

    def train_classifier(self, data):
        try:
            positive = self.cleaner.clean_tweets(data["positive"])
            negative = self.cleaner.clean_tweets(data["negative"])
            dataset = []
            for tokens in positive:
                dataset.append((dict([t, True] for t in tokens), +1))
            for tokens in negative:
                dataset.append((dict([t, True] for t in tokens), -1))
            random.shuffle(dataset)
            model = NaiveBayesClassifier.train(dataset)
            with open(self.get_model_path(), "wb") as analyser:
                analyser.write(pickle.dumps(model))
        except Exception as ex:
            print(ex)

    def load_classifier(self):
        with open(self.get_model_path(), "rb") as analyser:
            self.model = pickle.loads(analyser.read())
        self.loaded = True
        return self.model

    def analyse(self, tweets):
        if not self.loaded:
            return None
        filtered, cleaned = self.cleaner.clean_tweets(tweets)
        results = []
        for tokens in cleaned:
            predict = self.model.classify(dict([t, True] for t in tokens))
            results.append(predict)
        return results, filtered
