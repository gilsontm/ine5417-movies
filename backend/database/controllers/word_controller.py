from database import connection
from database.models import word_model
from database.models.word_model import Word


class WordController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def insert_many(self, analysis_id, words):
        parsed_words = []
        for key in words:
            data = {
                "text": key,
                "quantity": words[key],
                "analysis": analysis_id,
            }
            parsed_words.append(data)
        word_model.insert_many(parsed_words)

    def get_by_analysis(self, analysis_id):
        words = word_model.get_by_analysis(analysis_id)
        if words is None:
            return []
        results = [word.as_dict(recurse=False) for word in words]
        return results
