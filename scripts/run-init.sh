#!/bin/sh

source $PERIODIC_SCRIPT_PATH/envsetup.sh
source $PERIODIC_SCRIPT_PATH/helpers.sh

function log {
    systemd_log "$1" periodicpi-run
}

log 'Entering run state'

snapclient_state=$(extract_config $CONFIG_PATH/services.json snapclient)

if [ $snapclient_state == "True" ];
then
    log 'Starting snapclient service...'
    snapclient_init=$(systemctl start snapclient)
    if [ ! $snapclient_init == 0 ];
    then
        log 'Failed starting'
    else
        log 'Success'
    fi
fi

lircd_state=$(extract_config $CONFIG_PATH/services.json lircd)

if [ $lircd_state == "True" ];
then
    log 'Starting lircd...'
    lircd_init=$(systemctl start lircd)
    if [ ! $lircd_init == 0 ];
    then
        log 'Failed starting'
    else
        log 'Success'
    fi
fi
