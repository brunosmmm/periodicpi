#!/bin/sh

source $PERIODIC_SCRIPT_PATH/envsetup.sh

#run first boot tasks
$SCRIPT_PATH/hostapd-make.sh
$SCRIPT_PATH/setup_ir.sh

#set state file
touch /var/lib/periodicpi/initialsetupdone
