import json
import tornado.web
from database.controllers.user_controller import UserController

class LoginHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        pass

    def post(self):
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
