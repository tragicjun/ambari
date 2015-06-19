#!/bin/bash

BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

loginUser="ambari"
loginPass="ambari"

for host in `cat hosts`
do
	./service_cleaner.exp ${host} ${loginUser} ${loginPass}
done

