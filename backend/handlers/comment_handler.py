import json
from handlers.base_handler import BaseHandler
from database.controllers.entity_controller import EntityController
from database.controllers.comment_controller import CommentController


class CommentHandler(BaseHandler):
    def get(self):
        try:
            tmdb_id = self.get_argument("tmdb_id", None)
            comment_controller = CommentController()
            results = comment_controller.get_by_tmdb_id(tmdb_id)
            for result in results:
                result["created_at"] = result["created_at"].strftime("%H:%M %d/%m/%Y")
            self.write({"results": results})
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def post(self):
        try:
            request = json.loads(self.request.body)
            entity_controller = EntityController()
            entity = entity_controller.get_or_create(request["entity"])
            comment_controller = CommentController()
            comment_controller.insert(request["text"], request["user_id"], entity["id"])
        except Exception as ex:
            print(ex)
            self.set_status(500)
