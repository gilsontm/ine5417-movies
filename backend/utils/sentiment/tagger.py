import os
import nltk
import pickle
from nltk.corpus import floresta

def simplify_tag(tag):
    if "+" in tag:
        return tag[tag.index("+")+1:]
    return tag

def get_model_path():
    return f"{os.path.dirname(__file__)}/models/tagger.pkl"

def get_dataset():
    nltk.download("floresta")
    tsents = floresta.tagged_sents()
    tsents = [[(w.lower(), simplify_tag(t)) for (w,t) in sent] for sent in tsents if sent]
    return tsents

def train_model(dataset):
    tagger0 = nltk.DefaultTagger('n')
    tagger1 = nltk.UnigramTagger(dataset, backoff=tagger0)
    tagger2 = nltk.BigramTagger(dataset, backoff=tagger1)
    return tagger2

def train_and_save_model():
    dataset = get_dataset()
    model = train_model(dataset)
    dump = pickle.dumps(model)
    with open(get_model_path(), "wb") as tagger:
        tagger.write(dump)

def get_tagger():
    """
        Loads the POS-Tagger trained using the 'Floresta' dataset
    """
    with open(get_model_path(), "rb") as tagger:
        model = pickle.loads(tagger.read())
    return model

if __name__ == "__main__":
    train_and_save_model()
