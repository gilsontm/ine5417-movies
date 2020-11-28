import json
from handlers.base_handler import BaseHandler
from database.controllers.user_controller import UserController

class LoginHandler(BaseHandler):
    def post(self):
        if "/login" in self.request.uri:
            self.login()
        elif "/register" in self.request.uri:
            self.register()

    def login(self):
        try:
            request = json.loads(self.request.body)
            user_controller = UserController()
            user = user_controller.login(request["username"], request["password"])
            if user:
                self.write(user)
                self.set_status(200)
            else:
                self.set_status(401)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def register(self):
        try:
            user = json.loads(self.request.body)
            user_controller = UserController()
            success = user_controller.register(user)
            self.set_status(200 if success else 401)
        except Exception as ex:
            print(ex)
            self.set_status(500)