#!/bin/bash

LHOTSE_WEB_HOST=$1
LHOTSE_WEB_LISTEN_PORT=$2

DEFAULT_WEB_INSTALL_DIR=/usr/local/lhotse_web
DEFAULT_HTTPD_CONF=/etc/httpd/conf/httpd.conf

# Check whether the cgi listen port already exists
#PORT_EXIST=`netstat -nltp | grep "${LHOTSE_WEB_LISTEN_PORT}" | awk '{print $4}' | grep -E "\:${LHOTSE_WEB_LISTEN_PORT}\$" | wc -l`
#if [ $PORT_EXIST -ge 1 ]; then
#        echo "$LHOTSE_WEB_LISTEN_PORT already be used by other app, please choose another one."
#        exit -1
#fi
# Restart httpd service so that the new configurations can be applied
service httpd restart
