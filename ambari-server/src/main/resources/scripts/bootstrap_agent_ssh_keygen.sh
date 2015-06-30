#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

sshUser=$1
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    sudo /usr/sbin/groupadd tencent
    sudo /usr/sbin/useradd -g tencent -d /home/tencent -s /bin/bash -m tencent -p tencent
    homePath="/home/tencent"
fi

# generate sshkey file
if [ "${executor}" == "${sshUser}" ]
  then
    ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}
  else
    su -c "${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}" - ${sshUser}
fi
