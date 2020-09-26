import json
import tornado.web
from utils.apis import get_tmdb_api
from database.controllers.favorite_controller import FavoriteController

class SearchHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        pass

    def get(self):
        if "/search" in self.request.uri:
            self.search()
        elif "/info" in self.request.uri:
            self.info()

    def search(self):
        try:
            query = self.get_argument("query", None)
            search = get_tmdb_api().Search()
            promise = search.multi(query=query, language="pt")
            results = [result for result in search.results]
            self.write({"results": results})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)

    def info(self):
        try:
            api = get_tmdb_api()
            user_id = self.get_argument("user_id", None)
            entity = json.loads(self.get_argument("entity", None))

            favorite_controller = FavoriteController()
            is_favorite = favorite_controller.is_favorite(user_id, entity)

            if entity["media_type"] == "movie":
                model = api.Movies(entity["id"])
                related = model.similar_movies(language="pt")["results"]
            elif entity["media_type"] == "tv":
                model = api.TV(entity["id"])
                related = model.similar(language="pt")["results"]
            else:
                model = api.People(entity["id"])
                response = model.combined_credits(language="pt")
                related = response["cast"] + response["crew"]

            self.write({
                "info": model.info(language="pt"),
                "related": related,
                "is_favorite": is_favorite
            })
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)
