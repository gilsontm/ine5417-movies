from database import connection
from database.models import analysis_model
from database.models.analysis_model import Analysis


class AnalysisController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get_by_user_id(self, user_id):
        models = analysis_model.get_by_user_id(user_id)
        if models is None:
            return []
        dicts = [model.as_dict(exclude=[Analysis.user]) for model in models]
        return dicts

    def insert(self, user_id, entity_id):
        id = analysis_model.insert(user_id, entity_id)
        return id
