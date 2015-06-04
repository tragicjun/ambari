#!/bin/bash

LHOTSE_WEB_HOST=$1
LHOTSE_WEB_LISTEN_PORT=$2

DEFAULT_WEB_INSTALL_DIR=/usr/local/lhotse_web
DEFAULT_HTTPD_CONF=/etc/httpd/conf/httpd.conf

# Check to see whether the configuration exists
CONFIG_EXIST=`cat $DEFAULT_HTTPD_CONF | grep "/usr/local/lhotse_web$" | wc -l`

# Check to see whether the port is in use
PORT_EXIST=`cat $DEFAULT_HTTPD_CONF | grep -i "Listen $LHOTSE_WEB_LISTEN_PORT$" | wc -l`

echo "The config already exists: $CONFIG_EXIST, the port already exists: $PORT_EXIST"

# Append the new configuration if it's not configured
if [ $CONFIG_EXIST == 0 ]; then 
    # If configure a same port, need to return error messages. 
    if [ $PORT_EXIST -ge 1 ]; then
        echo "The port $LHOTSE_WEB_LISTEN_PORT is in use, please try another port"
        exit -1
    fi
    
    # Configure the httpd.conf so that it's able to accept requests
    echo "Listen $LHOTSE_WEB_LISTEN_PORT"                    >>          $DEFAULT_HTTPD_CONF
    echo "<VirtualHost *:$LHOTSE_WEB_LISTEN_PORT>"           >>          $DEFAULT_HTTPD_CONF
    echo "    DocumentRoot $DEFAULT_WEB_INSTALL_DIR"         >>          $DEFAULT_HTTPD_CONF
    echo "    ServerName $LHOTSE_WEB_HOST"                   >>          $DEFAULT_HTTPD_CONF
    echo "</VirtualHost>"                                    >>          $DEFAULT_HTTPD_CONF
else
    # Locate the document root line, it helps us locating other lines
    DOCUMENT_ROOT_LINE=`sed -n '/\/usr\/local\/lhotse_web$/=' $DEFAULT_HTTPD_CONF`
    PORT_LINE=`expr $DOCUMENT_ROOT_LINE - 1`
    SERVER_NAME_LINE=`expr $DOCUMENT_ROOT_LINE + 1`

    # Get the old settings
    PORT_VAR=`sed -n "$PORT_LINE p" $DEFAULT_HTTPD_CONF | awk -F ":" '{print $2}'`
    PORT_LENGTH=`echo | awk '{print length("'${PORT_VAR}'")}'`
    END_INDEX=`expr $PORT_LENGTH - 1`

    OLD_PORT=`echo | awk '{print substr("'${PORT_VAR}'", 1, '${END_INDEX}')}'`
    OLD_SERVER=`sed -n "$SERVER_NAME_LINE p" $DEFAULT_HTTPD_CONF | awk -F " " '{print $2}'`

    # Do the replacement if the configurations change
    if [ $LHOTSE_WEB_LISTEN_PORT != $OLD_PORT ]; then
        if [ $PORT_EXIST -ge 1 ]; then
            echo "The port $LHOTSE_WEB_LISTEN_PORT is in use by other applications, try other port"
            exit -2
        fi
 
        sed -i "s/Listen $OLD_PORT/Listen $LHOTSE_WEB_LISTEN_PORT/g" $DEFAULT_HTTPD_CONF
        sed -i "s/VirtualHost \*:$OLD_PORT/VirtualHost \*:$LHOTSE_WEB_LISTEN_PORT/g" $DEFAULT_HTTPD_CONF
    fi

    if [ $LHOTSE_WEB_HOST != $OLD_SERVER ]; then
        sed -i "s/ServerName $OLD_SERVER/ServerName $LHOTSE_WEB_HOST/g" $DEFAULT_HTTPD_CONF
    fi
fi

# Restart httpd service so that the new configurations can be applied
service httpd restart
