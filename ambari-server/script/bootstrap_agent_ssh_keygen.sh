#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

sshUser="ambari"
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    echo "${user} does not exists!"
    exit -1
fi

# generate sshkey file
if [ "${executor}" == "${sshUser}" ]
  then
    ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}
  else
    su -c "${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}" - ${sshUser}
fi
