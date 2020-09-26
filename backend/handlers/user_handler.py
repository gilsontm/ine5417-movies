import json
import tornado.web
from utils.apis import get_tmdb_api
from database.controllers.entity_controller import EntityController
from database.controllers.favorite_controller import FavoriteController

class UserHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')

    def options(self):
        pass

    def get(self):
        if "/favorite" in self.request.uri:
            self.get_favorites()

    def get_favorites(self):
        try:
            user_id = self.get_argument("user_id", None)
            favorite_controller = FavoriteController()
            favorites = favorite_controller.get_by_user_id(user_id)
            api = get_tmdb_api()
            results = []
            for favorite in favorites:
                tmdb_id = favorite["entity"]["tmdb_id"]
                media_type = favorite["entity"]["media_type"]
                if media_type == "movie":
                    model = api.Movies(tmdb_id)
                elif media_type == "tv":
                    model = api.TV(tmdb_id)
                else:
                    model = api.People(tmdb_id)
                info = model.info()
                info["media_type"] = media_type
                results.append(info)
            self.write({"results": results})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def put(self):
        if "/favorite" in self.request.uri:
            self.update_favorite()

    def update_favorite(self):
        try:
            request = json.loads(self.request.body)
            user_id = request["user_id"]
            entity_controller = EntityController()
            favorite_controller = FavoriteController()
            if request["favorite"]:
                entity = entity_controller.get_or_insert(request["entity"])
                favorite_controller.insert(user_id, entity["id"])
            else:
                entity = entity_controller.get(request["entity"])
                favorite_controller.remove(user_id, entity["id"])
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)



