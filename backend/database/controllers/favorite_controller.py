from database import connection
from database.models import favorite_model
from database.models import entity_model

class FavoriteController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get(self, user_id, entity):
        entity = entity_model.get(entity)
        if entity is None:
            return None
        favorite = favorite_model.get(user_id, entity.id)
        if favorite is None:
            return None
        return favorite.as_dict()

    def is_favorite(self, user_id, entity):
        entity = entity_model.get(entity)
        if entity is None:
            return False
        favorite = favorite_model.get(user_id, entity.id)
        return (favorite is not None)

    def insert(self, user_id, entity_id):
        id = favorite_model.insert(user_id, entity_id)
        return id

    def remove(self, user_id, entity_id):
        favorite_model.remove(user_id, entity_id)

    def get_by_user_id(self, user_id):
        models = favorite_model.get_by_user_id(user_id)
        if models is None:
            return []
        results = [model.as_dict() for model in models]
        return results
