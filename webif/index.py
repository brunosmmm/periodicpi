import bottle
import os
from bottle import route, run, view
import json
from periodicpy.wifitools.wifiinfo import WifiInfoDecoder, WifiInfo

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

def read_wifi_list():

    with open('/var/lib/periodicpi/wifi_scan.json', 'r') as scan_json:
        scan_results = json.load(scan_json)
        return scan_results

    return None

@route('/')
@view('index')
def index():
    scan_results = read_wifi_list()
    if scan_results == None:
        wifi_list = []
    else:
        wifi_list = [WifiInfo.from_dict(x) for x in scan_results['wifi_list']]
        
    return dict(scanlist=wifi_list, configmode=periodic_config_mode)

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
