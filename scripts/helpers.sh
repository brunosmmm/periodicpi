#!/bin/sh

#extract parameter from simple JSON configuration file
function extract_config  {
    cat $1 | python2 -c 'import json,sys; cfg=json.load(sys.stdin); print cfg["'$2'"]'
}

#log with systemd, argument 1 is message, argument 2 is origin
function systemd_log {
    echo "$1" | systemd-cat -t "$2"
}
