import tornado.ioloop
import tornado.web
from database.connection import setup_database
from handlers.login_handler import LoginHandler
from handlers.search_handler import SearchHandler


def make_app():
    return tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/register", LoginHandler),
        (r"/search", SearchHandler),
    ])

def main():
    setup_database()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
