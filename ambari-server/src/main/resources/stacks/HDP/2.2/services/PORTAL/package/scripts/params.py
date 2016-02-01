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



# soft link
portal_install_path = "/usr/local/tbds-portal"
portal_conf_path = "/usr/local/tbds-portal/api/application/config"
portal_conf_path_web = "/etc/httpd/conf.d/tbds-portal.conf"

new_portal_install_path = "/opt/tbds/portal"
new_portal_conf_path = "/etc/tbds/portal/config"
new_portal_conf_path_web = "/etc/tbds/portal/tbds-portal.conf"

# params
sso_server_hostname = default('/configurations/cluster-env/sso_server_hostname',"127.0.0.1")
sso_server_port = default('/configurations/cluster-env/sso_server_port',"8081")
sso_server_application = default('/configurations/cluster-env/sso_server_application',"cas")

portal_server_hostname = default('/configurations/cluster-env/portal_server_hostname',"127.0.0.1")
portal_server_port = default('/configurations/cluster-env/portal_server_port',"80")
portal_database_name = default('/configurations/portal-service/portal.database.name',"tbds")
portal_database_user = default('/configurations/portal-service/portal.database.user',"tbds")
portal_database_password = default('/configurations/portal-service/portal.database.password',"tbds")


# command
start_service = "service httpd restart"
stop_service = "rm -rf {0} && service httpd restart".format(portal_conf_path_web)

portal_service_host = default("/clusterHostInfo/portal_service_hosts", ["127.0.0.1"])[0]
portal_service_port = default("/configurations/portal-service/listen.port", 80)

portal_service_url = "http://{0}:{1}/tbds-portal/index.php".format(portal_service_host, portal_service_port)