#!/bin/sh

source $PERIODIC_SCRIPT_PATH/envsetup.sh
source $PERIODIC_SCRIPT_PATH/helpers.sh

#just call python script
python2 $PERIODIC_SCRIPT_PATH/../tools/node_init.py
