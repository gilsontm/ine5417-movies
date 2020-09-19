import bcrypt
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
        user = user_model.get_by_username(username)
        if user is None:
            return False
        if not bcrypt.checkpw(password.encode('utf8'), str(user.password).encode('utf8')):
            return False
        return user.as_dict(exclude=[User.password])

    def register(self, user):
        model = user_model.get_by_username(user["username"])
        if model is not None:
            return False
        user["password"] = bcrypt.hashpw(user["password"].encode('utf8'), bcrypt.gensalt())
        user_model.register(user)
        return True
