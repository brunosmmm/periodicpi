#!/bin/sh

source /usr/share/periodicpi/scripts/envsetup.sh
source /usr/share/periodicpi/scripts/helpers.sh

#log messages easily
function log {
    systemd_log "$1" periodicpi-init
}

#starting
log 'Starting low-level initialization'

#get config gpio num from configuration
config_gpio_num=$(extract_config $CONFIG_PATH/init.json config_gpio)
#get gpio active polarity
gpio_active_value=$(extract_config $CONFIG_PATH/init.json gpio_active_value)

#check if gpio is already exported
if [ ! -f /sys/class/gpio/gpio$config_gpio_num/value ];
then
    #export config mode force gpio
    echo $config_gpio_num > /sys/class/gpio/export
    log 'Exporting GPIO '$config_gpio_num
else
    log 'GPIO '$config_gpio_num' already exported'
fi

#wait
sleep 1

#read GPIO status
gpio_val=$(cat /sys/class/gpio/gpio$config_gpio_num/value)
if [ $gpio_val == $gpio_active_value ];
then
    log 'Configuration mode is set, initializing AP'
    $SCRIPT_PATH/enableap.sh
    echo '{ "config_mode" : true }' > /var/lib/periodicpi/config_status.json
else
    log 'Configuration mode not set, normal initialization'
    echo '{ "config_mode" : false }' > /var/lib/periodicpi/config_status.json
fi
