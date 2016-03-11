#!/bin/sh

source ./envsetup.sh

#run first boot tasks
$SCRIPT_PATH/hostapd-make.sh

#set state file
touch /var/lib/periodicpi/initialsetupdone
