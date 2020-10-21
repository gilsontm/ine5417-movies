from database import connection
from database.models import analysis_model


class AnalysisController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def insert(self, user_id, entity_id):
        id = analysis_model.insert(user_id, entity_id)
        return id

