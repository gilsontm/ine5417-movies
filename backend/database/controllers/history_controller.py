from database import connection
from database.models import history_model

class HistoryController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self,user_id):
        history = history_model.get(user_id)
        if history is None:
            return None
        return [h.title for h in history]

    def insert(self,user_id,title):
        id = history_model.insert(user_id,title)
        return id

    def remove(self,user_id,title):
        history_model.remove(user_id,title)