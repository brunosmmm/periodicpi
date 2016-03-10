from wifitools.scan import scan_and_parse

if __name__ == "__main__":
    scan_list = scan_and_parse('wlan0', True)
    print scan_list
