from database import connection
from database.models import comment_model
from database.models.comment_model import Comment


class CommentController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get_by_tmdb_id(self, tmdb_id):
        models = comment_model.get_by_tmdb_id(tmdb_id)
        if models is None:
            return []
        dicts = [model.as_dict() for model in models]
        return dicts

    def insert(self, text, user_id, entity_id):
        return comment_model.insert(text, user_id, entity_id)
