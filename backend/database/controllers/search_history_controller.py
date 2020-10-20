from database import connection
from database.models import search_history_model

class HistoryController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self,user_id):
        history = search_history_model.get(user_id)
        if history is None:
            return None
        return history.as_dict()

    def insert(self,user_id,title):
        id = search_history_model.insert(user_id,title)
        return id

    def remove(self,user_id,title):
        search_history_model.remove(user_id,title)