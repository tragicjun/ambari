#!/bin/bash

echo "Invoke configRunner.sh"

javaHome=$1
RUNNER_HOST=$2
CGI_BIN_LISTEN_PORT=$3

echo $javaHome $RUNNER_HOST $CGI_BIN_LISTEN_PORT

DEFAULT_HTTPD_CONF=/etc/httpd/conf.d/runner.conf
DEFAULT_GLOBAL_HTTPD_CONF=/etc/httpd/conf/httpd.conf
DEFAULT_RUNNER_DIR=/usr/local/lhotse_runners

# Configure the JAVA_HOME variable for runner hadoop client
cat /etc/hadoop/conf/hadoop-env.sh | awk -v var=$javaHome '{if($javaHome~/^#export JAVA_HOME=/){print "export JAVA_HOME="var}else print $0}' > my.hadoop-env.sh
cp my.hadoop-env.sh /etc/hadoop/conf/hadoop-env.sh
rm -rf my.hadoop-env.sh

echo "Configure the java home successfully"

PORT_EXIST=`cat $DEFAULT_GLOBAL_HTTPD_CONF | grep -iE "^Listen $CGI_BIN_LISTEN_PORT\$" | wc -l`

# Check whether the cgi listen port already exists
if [ $PORT_EXIST -ge 1 ]; then
        #shoud not add listen in DEFAULT_HTTPD_CONF
        sed -i 1d $DEFAULT_HTTPD_CONF
fi

# Release the cgi-bin codes
#cd $DEFAULT_RUNNER_DIR
#tar -xvzf getlog.tar.gz
#tar -xvzf tdcp.tar.gz

# Restart the httpd to enable the new configurations
service httpd restart
