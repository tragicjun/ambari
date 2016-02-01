#!/usr/bin/env bash
#
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#

mysqldservice=$1
mysqldbuser=$2
userhost=$3

remote_mysql_host=$4
remote_mysql_port=$5
remote_mysql_root_password=$6


myhostname=$(hostname -f)
sudo_prefix = "/var/lib/ambari-agent/ambari-sudo.sh -H -E"

# $sudo_prefix service $mysqldservice start
echo "Removing user $mysqldbuser@$userhost"
/var/lib/ambari-agent/ambari-sudo.sh su mysql -s /bin/bash - -c "mysql -h $remote_mysql_host -P $remote_mysql_port -u root -p$remote_mysql_root_password -e \"DROP USER '$mysqldbuser'@'$userhost';\""
/var/lib/ambari-agent/ambari-sudo.sh su mysql -s /bin/bash - -c "mysql -h $remote_mysql_host -P $remote_mysql_port -u root -p$remote_mysql_root_password -e \"flush privileges;\""
# $sudo_prefix service $mysqldservice stop
