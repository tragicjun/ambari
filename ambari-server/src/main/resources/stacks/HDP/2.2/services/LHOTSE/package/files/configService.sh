#!/bin/bash

SERVICE_JAVA_HOME=$1
SERVICE_LISTEN_PORT=$2

DEFAULT_SERVICE_PATH=/usr/local/lhotse_services

# Config the java home in startup.sh
cat $DEFAULT_SERVICE_PATH/bin/startup.sh | awk -v var=$SERVICE_JAVA_HOME '{if($SERVICE_JAVA_HOME~/^export JAVA_HOME=/){print "export JAVA_HOME="var}else print $0}' > startup.sh.tmp
cp startup.sh.tmp $DEFAULT_SERVICE_PATH/bin/startup.sh
rm -rf startup.sh.tmp

# Config the service listen port in service.xml
sed -i "s/Connector connectionTimeout=\"40000\" port=\"8088\"/Connector connectionTimeout=\"40000\" port=\"$SERVICE_LISTEN_PORT\"/g" $DEFAULT_SERVICE_PATH/conf/server.xml
