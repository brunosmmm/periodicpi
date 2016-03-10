import time
from daemon import runner
from periodicpy.wifitools.scan import scan_and_parse
from periodicpy.wifitools.wifiinfo import WifiInfoEncoder
import json

DEFAULT_SCAN_FILE = "/var/lib/periodicpi/wifi_scan.json"
DEFAULT_SCAN_INTERVAL = 10

class ScanWifi(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.pidfile_path = '/tmp/pwifi.pid'
        self.pidfile_timeout = 5

        self.scan_file = DEFAULT_SCAN_FILE
        self.scan_interval = DEFAULT_SCAN_INTERVAL

    def run(self):
        while True:
            scan_results = scan_and_parse('wlan0', True)

            with open(self.scan_file, 'w') as scan_json:
                scan_json.write(json.dumps(scan_results, cls=WifiInfoEncoder))

            time.sleep(self.scan_interval)

app = ScanWifi()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
