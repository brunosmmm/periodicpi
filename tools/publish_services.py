#!/usr/bin/python2

from daemon import runner
import json
import avahi
import signal
import time
from periodicpy.systemd.logging import log
from periodicpy.zeroconf import ZeroconfService

DEFAULT_CONFIG_FILE = '/etc/periodicpi/announce.json'

class Announcer(object):
    def __init__(self):

        self.stdin_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.pidfile_path = '/tmp/ppannounce.pid'
        self.pidfile_timeout = 5

        self.services = []
        self.service_dict = []

    def run(self):

        log('publishing services', 'periodic-publish')
        #handle SIGTERM
        def _handle_signal(signum, frame):
            for service in self.services:
                service.unpublish()

            exit(0)

        #read configuration files, get services
        self.service_dict = []
        self.services = []
        try:
            f = open(DEFAULT_CONFIG_FILE, 'r')
            config = json.load(f)
            self.service_dict = config['services']
        except IOError:
            return

        #configure signal handler
        signal.signal(signal.SIGTERM, _handle_signal)

        #get node element
        node_element = ''
        with open('/etc/periodicpi/node.json', 'r') as f:
            node = json.load(f)
            node_element = node['node_element']

        #announce services
        for service in self.service_dict:
            if service['enabled']:

                #announce "text"
                #by default put node element
                service_text = ['node_element={}'.format(node_element)]

                if 'text' in service:
                    service_text.extend(service['text'])
                
                log('publishing {}'.format(service['name']), 'periodic-publish')
                avahi_service = ZeroconfService(name='{} [{}]'.format(service['name'], node_element),
                                                port=int(service['port']),
                                                stype=service['type'],
                                                text=avahi.string_array_to_txt_array(service_text))
                avahi_service.publish()
                self.services.append(avahi_service)

        #do nothing!
        while True:
            time.sleep(1)

app = Announcer()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

