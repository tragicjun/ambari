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

from resource_management.libraries.functions.default import default
from resource_management import *

config = Script.get_config()


server_port = default('/configurations/yarn-api/yarn.api.http.port', 8089)
ftp_ip=default('/clusterHostInfo/ftp_server_hosts',["127.0.0.1"])[0]
ftp_port=default('/configurations/ftp/ftp.port', 2121)
ftp_user_name=default('/configurations/ftp/ftp.user', 'ftpadmin')
ftp_user_password=default('/configurations/ftp/ftp.password', '123456')
local_base_path='/data/tbds/taskexecutor'


config_path='/opt/tbds/taskexecutor/conf/'
start_cmd="su hdfs -c '/opt/tbds/taskexecutor/bin/task-executor.sh start'"
stop_cmd="su  hdfs -c '/opt/tbds/taskexecutor/bin/task-executor.sh stop'"
status_cmd=" su hdfs -c '/opt/tbds/taskexecutor/bin/task-executor.sh status'"
