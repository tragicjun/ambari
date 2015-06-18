#!/bin/bash

GOLDENEYE_WEB_LISTEN_PORT=$1

DEFAULT_WEB_INSTALL_DIR=/usr/local/goldeneye/goldeneye-web
DEFAULT_HTTPD_CONF=/etc/httpd/conf.d/ge.conf
DEFAULT_GLOBAL_HTTPD_CONF=/etc/httpd/conf/httpd.conf

PORT_EXIST=`cat $DEFAULT_GLOBAL_HTTPD_CONF | grep -iE "^Listen $GOLDENEYE_WEB_LISTEN_PORT\$" | wc -l`
# Check whether the cgi listen port already exists
if [ $PORT_EXIST -ge 1 ]; then
        #shoud not add listen in DEFAULT_HTTPD_CONF
        sed -i 1d $DEFAULT_HTTPD_CONF
fi
# Restart httpd service so that the new configurations can be applied
service httpd restart
