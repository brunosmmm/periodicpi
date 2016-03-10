#!/bin/sh

source /usr/share/periodicpi/scripts/envsetup.sh
source /usr/share/periodicpi/scripts/helpers.sh

#get config gpio num from configuration
config_gpio_num=$(extract_config $CONFIG_PATH/init.json config_gpio)

#check if gpio is already exported
if [ ! -f /sys/class/gpio/gpio$config_gpio_num/value ];
then
    #export config mode force gpio
    echo $config_gpio_num > /sys/class/gpio/export
    echo 'Exporting GPIO '$config_gpio_num | systemd-cat -t periodicpi-init
fi

#wait
sleep 1

#read GPIO status
gpio_val=$(cat /sys/class/gpio/gpio$config_gpio_num/value)
if [ $gpio_val == "0" ];
then
    echo 'Configuration mode is set, initializing AP' | systemd-cat -t periodicpi-init
    $SCRIPT_PATH/enableap.sh
    echo '{ "config_mode" : true }' > /var/lib/periodicpi/config_status.json
else
    echo 'Configuration mode not set, normal initialization' | systemd-cat -t periodicpi-init
    echo '{ "config_mode" : false }' > /var/lib/periodicpi/config_status.json
fi
