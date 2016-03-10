#!/bin/sh

#killall hostapd
#killall dnsmasq
systemctl stop hostapd.service
systemctl stop dnsmasq.service
systemctl stop lighttpd.service
python2 ../tools/wifiscantool.py  stop
