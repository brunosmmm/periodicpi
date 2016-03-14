#!/bin/sh

source $PERIODIC_SCRIPT_PATH/helpers.sh
source $PERIODIC_SCRIPT_PATH/envsetup.sh

#PeriodicPi suffix
pp=pp

#get hostname
node_element=$(extract_config $CONFIG_PATH/initial_setup.json node_element)
HOST=$node_element$pp
sed_cmd="s/__SSID_PLACEHOLDER__/"$HOST"-config/g"

#put hostname into SSID
sed $sed_cmd hostapd.conf > /etc/hostapd/hostapd.conf

#put node eleemnt in node.json
sed -ri 's/("node_element"\s*:\s*")([a-zA-Z0-9]+)("\s*,?)/\1'$node_element'\3/g' /etc/periodicpi/node.json

#set hostname temporarily and permanently
hostnamectl set-hostname $HOST
