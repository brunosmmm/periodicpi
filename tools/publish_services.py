from daemon import runner
import json
import avahi
import dbus
import signal
import time

DEFAULT_CONFIG_FILE = '/etc/periodicpi/announce.json'

class ZeroconfService(object):
    """A simple class to publish a network service with zeroconf using
    avahi.

    """

    def __init__(self, name, port, stype="_http._tcp",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text

    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(
                         bus.get_object(
                                 avahi.DBUS_NAME,
                                 avahi.DBUS_PATH_SERVER),
                        avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(avahi.DBUS_NAME,
                                   server.EntryGroupNew()),
                    avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g

    def unpublish(self):
        self.group.Reset()

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

        #handle SIGTERM
        def _handle_signal(signum, frame):
            for service in self.services:
                service.unpublish()

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

        #announce services
        for service in self.service_dict:
            if service['enabled']:
                avahi_service = ZeroconfService(name=service['name'], port=int(service['port']),
                                                stype=service['type'])
                avahi_service.publish()
                self.services.append(avahi_service)

        #do nothing!
        while True:
            time.sleep(1)

app = Announcer()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
