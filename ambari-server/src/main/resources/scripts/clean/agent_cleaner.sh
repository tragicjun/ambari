#!/bin/bash

> /var/lib/ambari-server/resources/scripts/clean/hosts
echo "get hosts"

clustername=`curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters?minimal_response=true" 2> /dev/null | grep cluster_name | awk -F':' '{print $2}' | sed  "s/[ \"]//g"`
echo $clustername

for host in `curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters/$clustername/hosts?minimal_response=true" 2> /dev/null | grep host_name | awk -F':' '{print $2}' | sed "s/[ \"]//g"`
do
  echo ${host} >> /var/lib/ambari-server/resources/scripts/clean/hosts
 
done
  



BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

loginUser="ambari"
loginPass="ambari"

sudo mkdir /tmp/clean

count=10
for host in `cat hosts`
do
  ./service_cleaner.exp ${host} ${loginUser} ${loginPass} 1>>/tmp/clean/${host}.log 2>&1 &
  sleep 5
  p_num=`ps -wef|grep service_cleaner | grep -v grep -c`
  echo "$p_num:: ${host}"

  while [ $p_num -ge $count ]
  do
      echo "$count"
      p_num=`ps -wef|grep service_cleaner | grep -v grep -c`
      sleep 5
      echo "$p_num:: sleep 2s..."
  done

done

wait