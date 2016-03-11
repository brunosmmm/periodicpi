#!/bin/sh

source ./helpers.sh
source ./envsetup.sh

#get hostname
HOST=$(extract_config $CONFIG_PATH/initial_setup.json hostname)
sed_cmd="s/__SSID_PLACEHOLDER__/"$HOST"-config/g"

#put hostname into SSID
sed $sed_cmd hostapd.conf > /etc/hostapd/hostapd.conf

#set hostname temporarily and permanently
hostnamectl set-hostname $HOST
