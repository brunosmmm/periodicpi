import time
from daemon import runner
from periodicpy.wifitools.scan import scan_and_parse
from periodicpy.wifitools.wifiinfo import WifiInfoEncoder
import json
import logging

DEFAULT_CONFIG_FILE = '/etc/periodicpi/wifiscantool.json'
DEFAULT_SCAN_FILE = "/var/lib/periodicpi/wifi_scan.json"
LOG_FILE = '/var/log/periodicpi/wifiscantool.log'
DEFAULT_SCAN_INTERVAL = 10

class ScanWifi(object):
    def __init__(self):

        #VERIFY if log file exists?

        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/tmp/pwifi.pid'
        self.pidfile_timeout = 5

        #put defaults
        self.scan_file = DEFAULT_SCAN_FILE
        self.scan_interval = DEFAULT_SCAN_INTERVAL

    def run(self):

        #setup logging
        self.logger = logging.getLogger('periodicpi.wifiscantool')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.info('Wi-fi scanning tool started')

        #try to open configuration file
        try:
            f = open(DEFAULT_CONFIG_FILE, 'r')
            config = json.loads(f.read())
            self.scan_file = config['scan_file']
            self.scan_interval = int(config['interval'])
            self.interface = config['interface']
        except IOError:
            self.logger.warn('Failed to open configuration file: {}'.format(DEFAULT_CONFIG_FILE))
        except Exception:
            self.logger.warn('Failed to parse configuration file')

        self.logger.info('Started scanning...')

        while True:
            scan_results = scan_and_parse(self.interface, True)

            with open(self.scan_file, 'w') as scan_json:
                json.dump({'interface' : self.interface, 'timestamp' : time.time(), 'wifi_list' : scan_results}, cls=WifiInfoEncoder, fp=scan_json)

            time.sleep(self.scan_interval)

app = ScanWifi()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
