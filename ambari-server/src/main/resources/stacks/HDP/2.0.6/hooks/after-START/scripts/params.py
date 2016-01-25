#coding=utf-8

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
import json

nginxExist = default("/clusterHostInfo/nginx_server_hosts", None)

components = ["GOLDENEYE_WEB", "LHOTSE_WEB", "NIFI_SERVER", "HUE_SERVER"]
component = default("/role", None)

command = default("/roleCommand", None)
commandParam = default("/hostLevelParams/custom_command", None)

nginxNeedReload = nginxExist and \
                  component in components and \
                  (command == "START" or command == "CUSTOM_COMMAND" and commandParam == "RESTART")

if nginxNeedReload:
  nginxHost = None if not nginxExist else nginxExist[0]
  serverHost = default("/clusterHostInfo/ambari_server_host", [None])[0]
  serverPort = str(default("/configurations/cluster-env/ambari_server_port", 8080))
  user = default("/configurations/cluster-env/cluster_manager", "admin")
  password = default("/configurations/cluster-env/cluster_manager_password", "admin")
  clusterName = default("/clusterName", None)

  baseCmd = "curl --user {0}:{1} -H 'X-Requested-By:{0}'".format(user, password)
  url = "http://{0}:{1}/api/v1/clusters/{2}/requests".format(serverHost, serverPort, clusterName)
  body = json.dumps({
    "RequestInfo": {
      "command": "RESTART",
      "context": "刷新Nginx配置",
      "operation_level": {
        "level": "SERVICE",
        "cluster_name": "{0}",
        "service_name": "NGINX"
      }
    },
    "Requests/resource_filters": [
      {
        "service_name": "NGINX",
        "component_name": "NGINX_SERVER",
        "hosts": "{1}"
      }
    ]
  }).replace("{0}", clusterName).replace("{1}", nginxHost)
  restartNginx = "{0} {1} -d '{2}'".format(baseCmd, url, body)
