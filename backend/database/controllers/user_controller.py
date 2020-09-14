from database import connection
from database.models import user_model
from database.models.user_model import User


class UserController:
    def __init__(self):
        connection.database.connect(reuse_if_open=True)

    def get_by_id(self, id):
        user = user_model.get_by_id(id)
        if user is None:
            return None
        return user.as_dict(exclude=[User.password])

    def login(self, username, password):
        raise NotImplementedError()
