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

goldeneye_web_pid_file = '/usr/local/goldeneye/goldeneye-web/web.pid'

#scripts
config_web_script = format("{tmp_dir}/configWeb.sh")
gri_ge_script = format("{tmp_dir}/gri_ge.sql")
gri_monitor_script = format("{tmp_dir}/gri_monitor.sql")
start_mysql_script = format("{tmp_dir}/startMySql.sh")


#golden eye web
goldeneye_web_listen_port = default("/configurations/goldeneye-web/listen.port", "80")[0]

#golden eye db
goldeneye_database_host = default("/clusterHostInfo/goldeneye-metadata-database_hosts", ["localhost"])[0]

goldeneye_data_dir = default("/configurations/goldeneye-metadata-database/data.dir", "/data/goldeneye/mysql_data")[0]
goldeneye_database_port = default("/configurations/goldeneye-metadata-database/database.port", 3306)[0]
goldeneye_database_username = default("/configurations/goldeneye-metadata-database/goldeneye.username", "root")[0]
goldeneye_database_password = default("/configurations/goldeneye-metadata-database/goldeneye.password", "")[0]


