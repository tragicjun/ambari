#!/bin/bash
executor=`whoami`
BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`
sshUser=$1
echo "[----- BOOTSTRAP -----]1. start to generate certificate of user:${sshUser}"
homePath=`cat /etc/passwd | grep ${sshUser}: | awk -F':' '{print $6}'`
if [ "${homePath}" == "" ]
  then 
    echo "[----- BOOTSTRAP -----]1.1 create ssh key user: ${sshUser}"
    /usr/sbin/groupadd ${sshUser}
    /usr/sbin/useradd -g ${sshUser} -d /home/${sshUser} -s /bin/bash -m ${sshUser}
    if [ $? -ne 0 ];then
      echo "[===== BOOTSTRAP-ERROR =====]create ssh key user[ ${sshUser} ] failed"
      exit -1
    fi
    homePath="/home/${sshUser}"
fi

# generate sshkey file
tries=3;
isSuccess=false;
for (( i=0; i<${tries}; i++ )); do
  if [ "${executor}" == "${sshUser}" ]; then
      echo "[----- BOOTSTRAP -----]1.2 execute ssh_keygen.exp: ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}"
      ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}
  else
      rm -f ${homePath}/.ssh/*
      echo "[----- BOOTSTRAP -----]1.2 execute ssh_keygen.exp: su - ${sshUser} -c ${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}"
      su - ${sshUser} -c "${currentPath}/bootstrap_agent_ssh_keygen.exp ${homePath}"
  fi
  sleep 3
  if ( test -s ${homePath}/.ssh/id_rsa ) && ( test -s ${homePath}/.ssh/id_rsa.pub ); then
    isSuccess=true;
    break
  fi
  echo "[===== BOOTSTRAP-ERROR =====]try generate ssh key file failed ${i} times"
done

if ! ${isSuccess}; then
  echo "[===== BOOTSTRAP-ERROR =====]generate ssh key file failed"
  exit -1
fi

# set the tbds server ssh login
cat ${homePath}/.ssh/id_rsa.pub >> ${homePath}/.ssh/authorized_keys
chmod 600 ${homePath}/.ssh/authorized_keys
chown ${sshUser}:${sshUser} ${homePath}/.ssh/authorized_keys
echo "[----- BOOTSTRAP -----]1. end generate certificate"
