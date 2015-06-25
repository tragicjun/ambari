#!/bin/bash
echo "step 1: server stop"
sudo ambari-server stop

echo "step 2: reset db"
sudo ambari-server reset

echo "step3: yum erase ambari-server"
sudo yum erase ambari-server

echo "step4: rm dir"
sudo rm -R /var/lib/ambari*
sudo rm -R /usr/lib/ambari*
sudo rm -R /var/log/ambari*
sudo rm -R /var/run/ambari*
sudo rm -R /usr/bin/ambari*
sudo rm -R /usr/sbin/ambari*
sudo rm -R /usr/lib/python2.6/site-packages/ambari*
sudo rm -R /usr/lib/python2.6/site-packages/resource_management
sudo rm -R /etc/ambari*

echo "step5: yum clean all"
sudo yum clean all