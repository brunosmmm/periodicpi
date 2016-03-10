#!/bin/sh

source /usr/share/periodicpi/scripts/envsetup.sh

#check if gpio is already exported
if [ ! -f /sys/class/gpio/gpio4/value ];
then
    #export config mode force gpio
    echo 4 > /sys/class/gpio/export
fi

sleep 1

#read GPIO status
gpio_val=$(cat /sys/class/gpio/gpio4/value)
if [ $gpio_val == "0" ];
then
    echo 'Configuration mode is set, initializing AP' | systemd-cat -t periodicpi-init
    $SCRIPT_PATH/enableap.sh
    echo '{ "config_mode" : true }' > /var/lib/periodicpi/config_status.json
else
    echo 'Configuration mode not set, normal initialization' | systemd-cat -t periodicpi-init
    echo '{ "config_mode" : false }' > /var/lib/periodicpi/config_status.json
fi
