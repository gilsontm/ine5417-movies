import nltk

def get_stemmer():
    nltk.download("rslp")
    stemmer = nltk.stem.RSLPStemmer()
    return stemmer
