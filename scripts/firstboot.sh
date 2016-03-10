#!/bin/sh

source /usr/share/periodicpi/scripts/envsetup.sh

#run first boot tasks
$SCRIPT_PATH/hostapd-make.sh

#set state file
touch /var/lib/periodicpi/initialsetupdone
