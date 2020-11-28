import nltk
from nltk.tokenize import word_tokenize
from utils.sentiment.stemmer import get_stemmer
from utils.sentiment.tagger import get_tagger


class Cleaner:
    def __init__(self):
        self.stemmer = get_stemmer()
        self.tagger = get_tagger()
        self.stopwords = self.get_stopwords()
        self.tags = [
            "n", "adj", "adv", "v-inf",
            "v-fin", "v-pcp", "v-ger",
            "conj-s", "conj-c",
        ]

    def get_stopwords(self):
        nltk.download("stopwords")
        words = nltk.corpus.stopwords.words("portuguese")
        words = list(filter(lambda w: len(w) > 2, words))
        return words

    def clean_tweets(self, tweets):
        is_valid = lambda w: len(w) > 2 and not (w.startswith("http") or w.startswith("@")) and not (w in self.stopwords)
        filtered = []
        for tweet in tweets:
            tokens = word_tokenize(tweet)
            tokens = [w.lower() for w in tokens]
            tokens = list(filter(is_valid, tokens))
            filtered.append(tokens)
        tagged = self.tagger.tag_sents(filtered)
        cleaned = []
        for tokens in tagged:
            tokens = [word for (word, tag) in tokens if tag in self.tags]
            tokens = [self.stemmer.stem(w) for w in tokens]
            cleaned.append(tokens)
        return filtered, cleaned
