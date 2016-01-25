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
nginx_server_ip = default("/clusterHostInfo/nginx_server_hosts", [None])[0]
nifi_or_nginx_server_ip = nginx_server_ip if nginx_server_ip else nifi_server_ip

portal_server_hostname=default("/configurations/cluster-env/portal_server_hostname", 'localhost')
portal_server_port=default("/configurations/cluster-env/portal_server_port", 80)
jar_path_url='http://' + portal_server_hostname + ':' + str(portal_server_port) + '/openapi/findFiles'

url='http://' + portal_server_hostname + ':' + str(portal_server_port) + '/openapi/getHostWanIp?localIP=' + nifi_or_nginx_server_ip
Logger.info(url)
res = urllib2.urlopen(url)
res_data=res.read()
Logger.info(res_data)
obj = json.loads(res_data)
code = obj.get("resultCode")
wanip = obj.get("resultData")
if '0'==code:
  nifi_or_nginx_server_ip = wanip
else:
  Logger.warn('get nifi server wanip failed :' + wanip)

nifi_user = config['configurations']['nifi-env']['nifi_user']
hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']
web_http_port = config['configurations']['nifi-site']['nifi.http.port']


#remote task executor
yarn_api_ip=  default("/clusterHostInfo/yarn_api_hosts", ["localhost"])[0]
yarn_api_port= default('/configurations/yarn-api/yarn.api.http.port', 8089)
yarn_api_url='http://' + yarn_api_ip + ':' + str(yarn_api_port) + '/task'

jstorm_api_ip=  default("/clusterHostInfo/jstorm_api_hosts", ["localhost"])[0]
jstorm_api_port= default("/configurations/jstorm-api/jstorm.api.http.port", 8085)
jstorm_api_url='http://' + jstorm_api_ip + ':' + str(jstorm_api_port) + '/task'

# Security-related params
sso_url =  default("/configurations/cluster-env/sso_url", "http://localhost:80/")
security_enabled = config['configurations']['cluster-env']['security_enabled']

#nifi-site
content_repository_directory = default('/configurations/nifi-site/content.repository.directory', './content_repository')
content_repository_period = default('/configurations/nifi-site/content.repository.period', '12 hours')
content_repository_max_usage_percentage = default('/configurations/nifi-site/content.repository.max.usage.percentage', '%50')

flowfile_repository_directory = default('/configurations/nifi-site/flowfile.repository.directory', './flowfile_repository')
provenance_repository_directory = default('/configurations/nifi-site/provenance.repository.directory', './provenance_repository')