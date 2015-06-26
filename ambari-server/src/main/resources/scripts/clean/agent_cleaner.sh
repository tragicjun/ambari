#!/bin/bash

> hosts
echo "get hosts"

clustername=`curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters?minimal_response=true" 2> /dev/null | grep cluster_name | awk -F':' '{print $2}' | sed  "s/[ \"]//g"`
echo $clustername

for host in `curl --user admin:admin "http://0.0.0.0:8080/api/v1/clusters/$clustername/hosts?minimal_response=true" 2> /dev/null | grep host_name | awk -F':' '{print $2}' | sed "s/[ \"]//g"`
do
  echo ${host} >> ./hosts
 
done
  


BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

loginUser="ambari"
loginPass="ambari"

count=10
num=0
for host in `cat hosts`
do
  ./service_cleaner.exp ${host} ${loginUser} ${loginPass} &
  num=$((num+1))
  echo ${host}
  if((num >= count)):
    echo "wait process finished"
    num=0
    wait
   fi
done

wait