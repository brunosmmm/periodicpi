#!/bin/sh

source ./envsetup.sh
source ./helpers.sh

function log {
    systemd_log "$1" periodicpi-run
}

log 'Entering run state'

snapclient_state=$(extract_config $CONFIG_PATH/services.json snapclient)

if [ snapclient_state == "True" ];
then
    log 'Starting snapclient service...'
    snapclient_init=$(systemctl start snapclient)
    if [ ! snapclient_init == 0 ];
    then
        log 'Failed starting'
    else
        log 'Success'
    fi
fi
