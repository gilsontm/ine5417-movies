from database import connection
from database.models import entity_model


class EntityController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self, entity):
        model = entity_model.get(entity)
        if model is None:
            return None
        return model.as_dict()

    def get_or_create(self, entity):
        model, _ = entity_model.get_or_create(entity)
        if model is None:
            return None
        return model.as_dict()
