import bottle
import os
from bottle import route, run, view
import json

class ConfigReadError(Exception):
    pass

def get_periodic_config_mode():
    """Verifies current operating mode"""
    try:
        config = open('/var/lib/periodicpi/config_status.json', 'r')
        current_cfg = config.read()
    except IOError:
        raise ConfigReadError('Could not read configuration file')

    current_cfg = json.loads(current_cfg)
    try:
        return current_cfg['config_mode']
    except KeyError:
        raise ConfigReadError('Invalid configuration file')

@route('/')
@view('index')
def index():
    return dict(scanlist=[], configmode=periodic_config_mode)

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
bottle.TEMPLATE_PATH.append(os.path.join(APP_ROOT, 'templates'))
app = bottle.default_app()
periodic_config_mode = False

if __name__ == "__main__":

    #read current mode
    try:
        periodic_config_mode = get_periodic_config_mode()
    except ConfigReadError:
        pass
    
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
