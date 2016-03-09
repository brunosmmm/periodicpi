import bottle
import os
from bottle import route, run, view

@route('/')
@view('index')
def index():
    return dict(hello='Hello World')

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
bottle.TEMPLATE_PATH.append(os.path.join(APP_ROOT, 'templates'))
app = bottle.default_app()

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
