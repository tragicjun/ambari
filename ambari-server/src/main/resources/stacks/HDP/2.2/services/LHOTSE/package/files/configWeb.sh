#!/bin/bash

LHOTSE_WEB_HOST=$1
LHOTSE_WEB_LISTEN_PORT=$2

DEFAULT_WEB_INSTALL_DIR=/usr/local/lhotse_web
DEFAULT_HTTPD_CONF=/etc/httpd/conf.d/lhotse_web.conf
DEFAULT_GLOBAL_HTTPD_CONF=/etc/httpd/conf/httpd.conf

PORT_EXIST=`cat $DEFAULT_GLOBAL_HTTPD_CONF | grep -iE "^Listen $LHOTSE_WEB_LISTEN_PORT\$" | wc -l`
# Check whether the cgi listen port already exists
if [ $PORT_EXIST -ge 1 ]; then
        #shoud not add listen in DEFAULT_HTTPD_CONF
        sed -i 1d $DEFAULT_HTTPD_CONF
fi
# Restart httpd service so that the new configurations can be applied
service httpd restart
