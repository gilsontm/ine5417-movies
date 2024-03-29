import tornado.ioloop
import tornado.web
from database.connection import setup_database
from handlers.login_handler import LoginHandler
from handlers.search_handler import SearchHandler
from handlers.user_handler import UserHandler
from handlers.analysis_handler import AnalysisHandler
from handlers.comment_handler import CommentHandler

def make_app():
    return tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/register", LoginHandler),
        (r"/search", SearchHandler),
        (r"/info", SearchHandler),
        (r"/favorite", UserHandler),
        (r"/history", SearchHandler),
        (r"/analysis", AnalysisHandler),
        (r"/analysis/list", AnalysisHandler),
        (r"/analysis/data", AnalysisHandler),
        (r"/analysis/export", AnalysisHandler),
        (r"/comments",CommentHandler),
    ])

def main():
    setup_database()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
