import json
import subprocess
from periodicpy.systemd.logging import log
from periodicpy.systemd.control import start_service, ServiceStartstopError

CONFIGURATION_PATH = '/etc/periodicpi'

if __name__ == "__main__":

    #read services
    contents = {}
    with open(CONFIGURATION_PATH+'/services.json', 'r') as f:
        contents = json.load(f)

    #enable services
    for service in contents['services']:
        if service['enabled']:
            log('starting {} service'.format(service['service_name']), 'node-init')

            try:
                start_service(service['service_name'])
                log('success', 'node-init')
            except ServiceStartStopError:
                log('faled starting', 'node-init')

    log('startup done', 'node-init')
