"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
import os

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()


# params
server_host = default('/clusterHostInfo/mysqlserver_hosts',["127.0.0.1"])[0]
server_port = default('/configurations/mysql-server/mysql.server.port',"3306")
server_root_password = default('/configurations/mysql-server/mysql.server.root.password',"root")
server_package_maxsize = default('/configurations/mysql-server/mysql.server.package.maxsize',"20971520")

# soft link
mysql_conf_path = "/etc/my.cnf"
mysql_data_path = "/var/lib/mysql"
mysql_log_path = "/var/lib/mysql"

new_mysql_conf_path = "/etc/tbds/mysql/my.cnf"
new_mysql_data_path = "/data/tbds/mysql"
new_mysql_log_path = "/data/tbds/mysql"

# command
init_server = "mysqladmin -P {0} -u root password '{1}'".format(server_port, server_root_password)
grant_base_privilege_to_all = "mysql -P {0} -u root -p{1} -e \"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{1}';\"" \
  .format(server_port, server_root_password)
grant_advanced_privilege_to_all = "mysql -P {0} -u root -p{1} -e \"GRANT GRANT OPTION, RELOAD ON *.* TO 'root'@'%' IDENTIFIED BY '{1}';\""\
  .format(server_port, server_root_password)

grant_base_privilege_to_local = "mysql -P {0} -u root -p{1} -e \"GRANT ALL PRIVILEGES ON *.* TO 'root'@'{2}' IDENTIFIED BY '{1}';\"" \
  .format(server_port, server_root_password, server_host)
grant_advanced_privilege_to_local = "mysql -P {0} -u root -p{1} -e \"GRANT GRANT OPTION, RELOAD ON *.* TO 'root'@'{2}' IDENTIFIED BY '{1}';\"" \
  .format(server_port, server_root_password, server_host)

flush_privileges = "mysql -P {0} -u root -p{1} -e \"FLUSH PRIVILEGES;\"" \
  .format(server_port, server_root_password)

start_server = "service mysql start"
stop_server = "service mysql stop"
status_server = "/usr/bin/mysqld"
reinstall_mysql = "yum reinstall mysql-server -y; echo"