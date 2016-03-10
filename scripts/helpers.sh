#!/bin/sh

#extract parameter from simple JSON configuration file
function extract_config  {
    cat $1 | python2 -c 'import json,sys; cfg=json.load(sys.stdin); print cfg["'$2'"]'
}
