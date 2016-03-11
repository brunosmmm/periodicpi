#!/bin/sh

#load stuff
source $PERIODIC_SCRIPT_PATH/envsetup.sh
source $PERIODIC_SCRIPT_PATH/helpers.sh

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

#setup IR remote output if enabled
remote_enabled=$(extract_config $CONFIG_PATH/init.json ir_out_enabled)

if [ $remote_enabled == "True" ];
then
    log 'IR output enbled, loading modules'
    #get IR output GPIO
    ir_out_gpio=$(extract_config $CONFIG_PATH/init.json ir_out_gpio)
    modprobe lirc_dev
    modprobe lirc_rpi gpio_out_pin=$ir_out_gpio
fi
