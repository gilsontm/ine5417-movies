import json
from peewee import DateTimeField
from utils.apis import get_tmdb_api
from handlers.base_handler import BaseHandler
from database.controllers.comment_controller import CommentController
from datetime import datetime

class CommentHandler(BaseHandler):
    def get(self):
        self.comment()

    def post(self):
        try:
            request = json.loads(self.request.body)
            user_id = request["user_id"]
            text = request["text"]
            print(text)
            entity_id = request["entity_id"]
            comment_controller = CommentController()
            comment_controller.insert(text,user_id,entity_id)
        except Exception as ex:
            self.set_status(500)
            raise

    def comment(self):
        try:
            entity_id = self.get_argument("entity", None)
            comment_controller = CommentController()
            results = comment_controller.get_by_entity_id(entity_id)
            print(results)
            for result in results:
                result["created_at"] = str(result["created_at"])
            print(results)

            self.write({"results": results})
        except Exception as ex:
            self.set_status(500)
            raise