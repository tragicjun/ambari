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
import socket
from nginx_config import nginx_config

config = Script.get_config()

nginx_start_command = "/etc/init.d/nginx start"
nginx_stop_command = "/etc/init.d/nginx stop"

nginx_conf_path = "/etc/nginx/"
default_conf_path = "/etc/nginx/conf.d/"

nginx_service = "nginx"

nginx_server_host = socket.gethostbyname(socket.gethostname())
nginx_server_port = default('/configurations/nginx-config/nginx.port',8080)
nginx_log_path = default('/configurations/nginx-config/nginx.log.path','/data/nginx/log/')
nginx_errorlog_level = default('/configurations/nginx-config/nginx.errorlog.level','crit')

nginx_log_accesslog = format("{nginx_log_path}/access.log")
nginx_log_errorlog = format("{nginx_log_path}/error.log")

# refractor service path

nginx_install_path = "/var/cache/nginx"
nginx_config_path = "/etc/nginx"
nginx_log_path = default("/configurations/nginx-config/nginx.log.path", "/data/nginx/log")

new_nginx_install_path = "/opt/tbds/nginx"
new_nginx_config_path = "/etc/tbds/nginx"
new_nginx_log_path = "/var/log/tbds/nginx/server"


cpu_cores = Toolkit.get_cpu_cores()
worker_connections = default("/configurations/nginx-config/nginx.worker.connections", "1024")
upstream_keepalive = default("/configurations/nginx-config/nginx.upstream.keepalive", "2000")
(servers, locations) = nginx_config().generate_default()