import json
import tornado.web
from utils.apis import get_tmdb_api

class SearchHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        pass

    def get(self):
        try:
            query = self.get_argument("query", None)
            search = get_tmdb_api().Search()
            promise = search.multi(query=query)
            results = [result for result in search.results]
            self.write({"results": results})
            self.set_status(200)
        except Exception as ex:
            print(ex)
            self.set_status(500)