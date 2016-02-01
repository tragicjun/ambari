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
server_port = default('/configurations/webshell-server/server.port',"80")
server_url_prefix = default('/configurations/webshell-server/server.url.prefix',"/ssh")
server_users = default('/configurations/webshell-server/server.users',"/opt/gateone/users")
server_host = default('/clusterHostInfo/webshell_server_hosts',["127.0.0.1"])[0]
server_session_dir = default('/configurations/webshell-server/server.session.dir',"/tmp/gateone")
server_host_wanip = server_host
server_logfile_maxsize = default('/configurations/webshell-server/server.logfile.maxsize',"104857600")
server_logfile_dir = default('/configurations/webshell-server/server.logfile.dir',"/opt/gateone/logs")
server_logfile_file = server_logfile_dir + "/webserver.log"

# soft link
webshell_install_path = "/opt/gateone"
webshell_conf_path = webshell_install_path + "/server.conf"
webshell_log_path = server_logfile_dir
webshell_data_path_users = server_users
webshell_data_path_session = server_session_dir

new_webshell_install_path = "/opt/tbds/webshell"
new_webshell_conf_path = "/etc/tbds/webshell/server.conf"
new_webshell_log_path = "/var/log/tbds/webshell/log"
new_webshell_data_path_users = "/data/tbds/webshell/users"
new_webshell_data_path_session = "/data/tbds/webshell/session"

# command
webshell_bin_path = webshell_install_path +"/gateone.py"
start_server = "(cd {0}; {1}&) &> /dev/null".format(webshell_install_path, webshell_bin_path)
stop_server = "cd {0}; {1} --kill &> /dev/null; echo".format(webshell_install_path, webshell_bin_path)
status_server = webshell_bin_path
server_url = "https://{0}:{1}{2}".format(server_host, server_port, server_url_prefix)