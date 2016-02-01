#!/usr/bin/env python
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
from ambari_commons.constants import AMBARI_SUDO_BINARY
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management.libraries.functions.default import default
from resource_management.libraries.script import Script
from resource_management.libraries.functions import default, format

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

root_dir = "/usr/local/grafana"
conf_dir = root_dir + "/conf"
grafana_user = "root"
grafana_group = "root"
tmp_data_dir = "data"
logs_dir = "data/logs"
#defaults.ini
http_port = config['configurations']['defaults']['http.port']
db_username = config['configurations']['defaults']['db.username']
db_password = config['configurations']['defaults']['db.password']

db_type = "mysql"
db_name = "grafana"
#db_host = config['configurations']['defaults']['db.host']
db_host = default("/clusterHostInfo/mysqlserver_hosts", ["127.0.0.1"])[0]
#db_port = config['configurations']['defaults']['db.port']
db_port = default("/configurations/mysql-server/mysql.server.port", "3306")



#init sql
init_sql_script = format("{tmp_dir}/init.sql")
start_mysql_script = format("{tmp_dir}/startMySql.sh")
