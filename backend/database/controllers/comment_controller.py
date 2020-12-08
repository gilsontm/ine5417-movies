from database import connection
from database.models import comment_model
from database.models.comment_model import Comment


class CommentController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get_by_entity_id(self, entity_id):
        models = comment_model.get_by_entity_id(entity_id)
        if models is None:
            return []
        dicts = [model for model in models]
        return dicts

    def insert(self, comment,user_id,entity_id):
        return comment_model.insert(comment,user_id,entity_id)

    def remove(self, comment_id):
        return comment_model.remove(comment_id)
