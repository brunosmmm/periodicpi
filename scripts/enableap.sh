#!/bin/sh

#force wlan ip
ifconfig wlan0 up 1.1.1.1 netmask 255.255.255.0
sleep 2

#start dnsmasq
#dnsmasq
systemctl start dnsmasq.service

#start hostapd
#hostapd -B /etc/hostapd/hostapd.conf
systemctl start hostapd.service

#start web server
systemctl start lighttpd.service
