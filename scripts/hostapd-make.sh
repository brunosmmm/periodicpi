#!/bin/sh

#get hostname
HOST=$(hostname)
sed_cmd="s/__SSID_PLACEHOLDER__/"$HOST"-config/g"

#put hostname into SSID
sed $sed_cmd hostapd.conf > /etc/hostapd/hostapd.conf

