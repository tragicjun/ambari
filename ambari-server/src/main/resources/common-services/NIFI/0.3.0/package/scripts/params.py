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
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management.libraries.functions.default import default
from resource_management.core.logger import Logger

import status_params
import json
import urllib2

# server configurations
config = Script.get_config()

stack_name = default("/hostLevelParams/stack_name", None)

version = default("/commandParams/version", None)

stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
hdp_stack_version = format_hdp_stack_version(stack_version_unformatted)

nifi_bootstrap_conf_template = config['configurations']['nifi-env']['content']

nifi_install_dir = '/opt/tbds/nifi/'
nifi_bin = '/opt/tbds/nifi/bin/nifi.sh'
nifi_conf_dir = "/opt/tbds/nifi/conf"
nifi_log_dir = "/opt/tbds/nifi/logs"
nifi_pid_file = "/opt/tbds/nifi/bin/nifi.pid"

new_nifi_config_path = "/etc/tbds/nifi"
new_nifi_data_path = "/data/tbds/nifi"
new_nifi_log_path = "/var/log/tbds/nifi"

nifi_server_ip = default("/clusterHostInfo/nifi_server_hosts", ["localhost"])[0]

portal_server_hostname=default("/configurations/cluster-env/portal_server_hostname", 'localhost')
portal_server_port=default("/configurations/cluster-env/portal_server_port", 80)
url='http://' + portal_server_hostname + ':' + str(portal_server_port) + '/openapi/getHostWanIp?localIP=' + nifi_server_ip
Logger.info(url)
res = urllib2.urlopen(url)
res_data=res.read()
Logger.info(res_data)
obj = json.loads(res_data)
code = obj.get("resultCode")
wanip = obj.get("resultData")
if '0'==code:
  nifi_server_wanip = wanip
else:
  Logger.warn('get nifi server wanip failed :' + wanip)
  nifi_server_wanip = nifi_server_ip

nifi_user = config['configurations']['nifi-env']['nifi_user']
hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']
web_http_port = config['configurations']['nifi-site']['nifi.http.port']

# Security-related params
sso_url =  default("/configurations/cluster-env/sso_url", "http://localhost:80/")
security_enabled = config['configurations']['cluster-env']['security_enabled']