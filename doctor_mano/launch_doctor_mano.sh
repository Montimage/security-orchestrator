#!/bin/bash

# Usage
#-------
if [ $# -ne 2 ]
then
    echo Usage: $0 tosca_template nfvo_host:nfvo_port
    exit 1
fi


TOSCA_FILE_PATH=$1
NFVO_HOST_PORT=$2
NFVO_DIR=/Users/long/workspace/pro/mano_v3/mano/nfvo
echo "Starting doctor MANO ... "
echo "Starting doctor Orchestrator ... "
rm deploy_log
rm pit_log
python3 $NFVO_DIR/nfvo_server.py $TOSCA_FILE_PATH $NFVO_HOST_PORT
