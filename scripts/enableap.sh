#!/bin/sh

source $PERIODIC_SCRIPT_PATH/envsetup.sh
source $PERIODIC_SCRIPT_PATH/helpers.sh

function log {
    systemd_log "$1" periodicpi-configap
}

log 'Setting up Config mode AP'

#get parameters
ap_iface=$(extract_config $CONFIG_PATH/ap_config.json interface)
ap_ip=$(extract_config $CONFIG_PATH/ap_config.json host_ip)

#force wlan ip
ifconfig $ap_iface up $ap_ip netmask 255.255.255.0
sleep 2

#start dnsmasq
#dnsmasq
systemctl start dnsmasq.service

#start hostapd
#hostapd -B /etc/hostapd/hostapd.conf
systemctl start hostapd.service

#start web server
#systemctl start lighttpd.service

#scan for wi-fi continuously
python2 ../tools/wifiscantool.py start
