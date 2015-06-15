#!/bin/bash

BINDIR=`dirname "$0"`
cd $BINDIR
currentPath=`pwd`

#create the ambari user
name="ambari"
password="ambari"
home_root="/home"

if [ ! -d ${home_root} ]; then
  echo "$home_root does not exists"
  exit -1;
fi
if cat /etc/passwd | awk -F : '{print $1}' | grep ${name} >/dev/null 2>&1
  then
    echo "the ${name} user has always exist"
  else
    pass=$(perl -e 'print crypt($ARGV[0], "wtf")' ${password})
    /usr/sbin/groupadd ${name}
    /usr/sbin/useradd -g ${name} -d ${home_root}/${name} -s /bin/bash -m ${name} -p ${pass}
fi
if [ ! -d ${home_root}/${name} ]
  then
    mkdir -p ${home_root}/${name}
fi
chown -R ${name}:${name} ${home_root}/${name}

#copy the pub file to ambari's .ssh directory
sshPath="${home_root}/${name}/.ssh"
if [ ! -d ${sshPath} ]
  then
    mkdir -p ${sshPath}
fi
cp ${currentPath}/id_rsa.pub ${sshPath}
cat ${sshPath}/id_rsa.pub >> ${sshPath}/authorized_keys
chmod 600 ${sshPath}/authorized_keys
chown ${name}:${name} ${sshPath}/authorized_keys
chmod 700 ${sshPath}
chown ${name}:${name} ${sshPath}

chmod 200 /etc/sudoers
echo "ambari ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers