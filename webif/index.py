import bottle
import os
from bottle import route, run, view, request
import json
from periodicpy.wifitools.wifiinfo import WifiInfoDecoder, WifiInfo
from periodicpy.plugmgr import ModuleManager
import logging

CONFIGURATION_PATH = '/etc/periodicpi'

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

@route('/status/node')
def get_info():

    #read node.json file
    contents = {}
    with open(CONFIGURATION_PATH+'/node.json', 'r') as f:
        contents = json.load(f)

    #add dynamic information
    #uptime, etc
    
    return contents

@route('/status/services')
def get_services():

    #read services.json file
    contents = {}
    with open(CONFIGURATION_PATH+'/services.json', 'r') as f:
        contents = json.load(f)
    
    return contents

#get active modules
@route('/status/active_plugins')
def report_plugins():
    #create module list
    mod_list = {}
    for inst_name in modman.get_loaded_module_list():
        mod_list[inst_name] = modman.get_instance_type(inst_name)

    return mod_list

#dump module structure
@route('/plugins/<mod_name>/structure')
def report_module(mod_name):
    return modman.get_module_structure(mod_name)


#get/set a property
@route('/plugins/<inst_name>/<prop_name>')
def get_set_property(inst_name, prop_name):
    try:
        return modman.get_module_property(inst_name, prop_name)
    except Exception:
        return {'status' : 'error'}

#execute method
@route('/plugins/<inst_name>/<method_name>', method='POST')
def run_method(inst_name, method_name):

    method_args = request.POST['method_args']

    logger.debug('executing method "{}" of instance "{}"; args = {}'.format(method_name, inst_name, method_args))   

    #make dictionary from argument string
    arg_dict = {}
    arg_list = method_args.split(',')
    for arg in arg_list:
        arg_name, arg_value = arg.split('=')
        arg_dict[arg_name] = arg_value
        
    ret = modman.call_module_method(inst_name, method_name, **arg_dict)
    
    return ret

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
bottle.TEMPLATE_PATH.append(os.path.join(APP_ROOT, 'templates'))
app = bottle.default_app()
periodic_config_mode = False
modman = ModuleManager('webif', '/usr/share/periodicpi/plugins')
logger = logging.getLogger('webif')

if __name__ == "__main__":

    #logging
    logging.basicConfig(level=logging.DEBUG,
                        filename='/var/log/periodicpi/webif.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    #read current mode
    try:
        periodic_config_mode = get_periodic_config_mode()
    except ConfigReadError:
        pass

    #load plugins according to configuration
    plug_conf = {}
    with open(CONFIGURATION_PATH+'/plugins.json', 'r') as f:
        plug_conf = json.load(f)

    modman.discover_modules()
    
    for plugin in plug_conf['load_plugins']:
        if 'args' not in plugin:
            args = {}
        else:
            if plugin['args'] == None:
                args = {}
            else:
                args = plugin['args']

        try:
            modman.load_module(plugin['id'], **args)
        except Exception:
            raise #for now
        
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()
