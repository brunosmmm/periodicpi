import time
import daemon
from periodicpy.wifitools.scan import scan_and_report

with daemon.DaemonContext():
    scan_and_report()
