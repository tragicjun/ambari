#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

# generate sshkey file
if [ "${executor}" == "ambari" ]
  then
    ${currentPath}/bootstrap_agent_ssh_keygen.exp
  else
    su -c "${currentPath}/bootstrap_agent_ssh_keygen.exp" - ambari
fi
