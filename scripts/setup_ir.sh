#!/bin/sh

source $PERIODIC_SCRIPT_PATH/envsetup.sh
source $PERIODIC_SCRIPT_PATH/helpers.sh

ir_out_gpio=$(extract_config $CONFIG_PATH/initial_setup.json ir_out_gpio)
sed -ri 's/(dtoverlay=lirc-rpi,gpio_out_pin=)([0-9]+)/\1'$ir_out_gpio'/g' /boot/config.txt
