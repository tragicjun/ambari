#!/bin/bash

echo "Invoke configRunner.sh"

javaHome=$1
RUNNER_HOST=$2
CGI_BIN_LISTEN_PORT=$3

echo $javaHome $RUNNER_HOST $CGI_BIN_LISTEN_PORT

DEFAULT_HTTPD_CONF=/etc/httpd/conf/httpd.conf
DEFAULT_RUNNER_DIR=/usr/local/lhotse_runners

# Configure the JAVA_HOME variable for runner hadoop client
cat /etc/hadoop/conf/hadoop-env.sh | awk -v var=$javaHome '{if($javaHome~/^#export JAVA_HOME=/){print "export JAVA_HOME="var}else print $0}' > my.hadoop-env.sh
cp my.hadoop-env.sh /etc/hadoop/conf/hadoop-env.sh
rm -rf my.hadoop-env.sh

echo "Configure the java home successfully"

# Check whether this settings already exists in httpd conf file
CONFIG_EXIST=`cat $DEFAULT_HTTPD_CONF | grep "/usr/local/lhotse_runners/getlog/$" | wc -l`

# Check whether the cgi listen port already exists
PORT_EXIST=`cat $DEFAULT_HTTPD_CONF | grep -i "Listen $CGI_BIN_LISTEN_PORT$" | wc -l`

echo "The config already exists: $CONFIG_EXIST, the port already exists: $PORT_EXIST"

# If this is the first time to set configurations, just append
if [ $CONFIG_EXIST == 0 ]; then
    # If the port already specified, print error message and exit
    if [ $PORT_EXIST -ge 1 ]; then
        echo "$PORT_EXIST already specified in $DEFAULT_HTTPD_CONF, please choose another one."
        exit -1
    fi

    # Configure the httpd.conf so that it's able to accept requests
    echo       ""                                                                   >>          $DEFAULT_HTTPD_CONF
    echo       "Listen $CGI_BIN_LISTEN_PORT"                                        >>          $DEFAULT_HTTPD_CONF
    echo       "<VirtualHost *:$CGI_BIN_LISTEN_PORT>"                               >>          $DEFAULT_HTTPD_CONF
    echo       "    ServerName $RUNNER_HOST"                                        >>          $DEFAULT_HTTPD_CONF
    echo       "    ScriptAlias /cgi-bin/ /usr/local/lhotse_runners/getlog/"        >>          $DEFAULT_HTTPD_CONF
    echo       "    <Directory \"/usr/local/lhotse_runners/getlog/\">"              >>          $DEFAULT_HTTPD_CONF
    echo       "      AllowOverride None"                                           >>          $DEFAULT_HTTPD_CONF
    echo       "      Options +ExecCGI"                                             >>          $DEFAULT_HTTPD_CONF
    echo       "      Order allow,deny"                                             >>          $DEFAULT_HTTPD_CONF
    echo       "      Allow from all"                                               >>          $DEFAULT_HTTPD_CONF
    echo       "    </Directory>"                                                   >>          $DEFAULT_HTTPD_CONF
    echo       "</VirtualHost>"                                                     >>          $DEFAULT_HTTPD_CONF
else 
    # Locate the document root line, it helps us locating other lines
    DOCUMENT_ROOT_LINE=`sed -n '/\/usr\/local\/lhotse_runners\/getlog\/$/=' $DEFAULT_HTTPD_CONF`
    PORT_LINE=`expr $DOCUMENT_ROOT_LINE - 2`
    SERVER_NAME_LINE=`expr $DOCUMENT_ROOT_LINE - 1`
 
    # Get the old settings
    PORT_VAR=`sed -n "$PORT_LINE p" $DEFAULT_HTTPD_CONF | awk -F ":" '{print $2}'`
    PORT_LENGTH=`echo | awk '{print length("'${PORT_VAR}'")}'`
    END_INDEX=`expr $PORT_LENGTH - 1`
 
    OLD_PORT=`echo | awk '{print substr("'${PORT_VAR}'", 1, '${END_INDEX}')}'`
    OLD_SERVER=`sed -n "$SERVER_NAME_LINE p" $DEFAULT_HTTPD_CONF | awk -F " " '{print $2}'`
  
    # Do the replacement if the configurations change
    if [ $CGI_BIN_LISTEN_PORT != $OLD_PORT ]; then
        if [ $PORT_EXIST -ge 1 ]; then
            echo "The port $CGI_BIN_LISTEN_PORT is in use by other applications, try other port"
            exit -2
        fi
  
        sed -i "s/Listen $OLD_PORT/Listen $CGI_BIN_LISTEN_PORT/g" $DEFAULT_HTTPD_CONF
        sed -i "s/VirtualHost \*:$OLD_PORT/VirtualHost \*:$CGI_BIN_LISTEN_PORT/g" $DEFAULT_HTTPD_CONF
    fi
  
    if [ $RUNNER_HOST != $OLD_SERVER ]; then
        sed -i "s/ServerName $OLD_SERVER/ServerName $RUNNER_HOST/g" $DEFAULT_HTTPD_CONF
    fi
fi

# Release the cgi-bin codes
cd $DEFAULT_RUNNER_DIR
tar -xvzf getlog.tar.gz

# Restart the httpd to enable the new configurations
service httpd restart
