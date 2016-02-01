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
from resource_management import *

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

stack_name = default("/hostLevelParams/stack_name", None)

version = default("/commandParams/version", None)

stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
hdp_stack_version = format_hdp_stack_version(stack_version_unformatted)

hue_install_dir = '/opt/tbds/hue'
hue_bin = hue_install_dir + '/build/env/bin/supervisor'
hue_admin_bin = hue_install_dir + '/build/env/bin/hue'
hue_conf_dir = "/opt/tbds/hue/desktop/conf"
hue_log_dir = "/opt/tbds/hue/logs"
hue_pid_file = "/opt/tbds/hue/hue.pid"
hue_init_flag = hue_install_dir + "/initialized"
hue_django_settings = hue_install_dir + "/desktop/core/src/desktop/settings.py"

new_hue_config_path = "/etc/tbds/hue"
new_hue_data_path = "/data/tbds/hue"
new_hue_log_path = "/var/log/tbds/hue"

hue_user = config['configurations']['hue-env']['hue_user']
hostname = config['hostname']
user_group = config['configurations']['cluster-env']['user_group']
java64_home = config['hostLevelParams']['java_home']
http_port = config['configurations']['hue-site']['http.port']

#hadoop services' addresses
namenode_http_address = config['configurations']['hdfs-site']['dfs.namenode.http-address']
fs_defaultFS = config['configurations']['core-site']['fs.defaultFS']
hive_host = default('/clusterHostInfo/hive_server_host',['localhost'])[0]
hive_port = default('/configurations/hive-site/hive.server2.thrift.port',"10000")
thive_host = default('/clusterHostInfo/thive_server_hosts',['localhost'])[0]
thive_port = default('/configurations/thive-config-env/thive.server.port',"10002")
thive_plc_user = default('/configurations/thive-config-env/hive.plc.user',"thive")
thive_plc_password = default('/configurations/thive-config-env/hive.plc.password',"thive")
yarn_rm_url = 'http://' + default('/configurations/yarn-site/yarn.resourcemanager.webapp.address', "localhost:8088")
livy_server_host = default('/clusterHostInfo/spark_livy_server_hosts', ['localhost'])[0]
livy_server_port = default('/configurations/livy-defaults/livy.server.port',"8998")
spark_jdbc_server_host = default('/clusterHostInfo/spark_jdbc_server_hosts',['localhost'])[0]
spark_jdbc_server_port = default('/configurations/spark-defaults/spark.hive.server2.thrift.port',"10002")
hive_metastore_warehouse_dir = default('/configurations/hive-site/hive.metastore.warehouse.dir',"/apps/hive/warehouse")

gp_master_host = default('/clusterHostInfo/gp_master_hosts', ['localhost'])[0]
gp_master_port = default('/configurations/gp-site/master.port', "5432")

sso_cas_url = default('/configurations/cluster-env/sso_url',"https://127.0.0.1:8080/cas") + "/"
hue_admin_user = default('/configurations/cluster-env/cluster_manager',"admin")

# Added by junz for sync user-group from LDAP
ldap_url = config['configurations']['cluster-env']['ldap_url']
if ldap_url:
    hue_middleware = 'useradmin.middleware.LdapSynchronizationMiddleware'
else:
    ldap_url = 'ldap://127.0.0.1:389'
    hue_middleware = ''

zookeeper_host = default('/clusterHostInfo/zookeeper_hosts', ['localhost'])
zk_address = zookeeper_host[0] + ":" + default('/configurations/zoo-cfg/clientPort', "2181")

# Security-related params
security_enabled = config['configurations']['cluster-env']['security_enabled']

# We temporarily use the mysql instance of Hive
hive_metastore_user_name = config['configurations']['hive-site']['javax.jdo.option.ConnectionUserName']
hive_metastore_user_passwd = config['configurations']['hive-site']['javax.jdo.option.ConnectionPassword']
hive_metastore_host = default('/clusterHostInfo/hive_mysql_host', ['localhost'])[0]

hue_database_config_script = format("{tmp_dir}/startMySql.sh")
hue_database_host = default("/clusterHostInfo/mysqlserver_hosts", ["127.0.0.1"])[0]
hue_database_port = default("/configurations/mysql-server/mysql.server.port", "3306")
hue_database_schema_path = "NA"
hue_database_rootusername = "root"
hue_database_rootuserpassword = default("/configurations/mysql-server/mysql.server.root.password", "root")
hue_database_username = "hue"
hue_database_password = "hue"
hue_database_name = "hue"
hue_database_engine = "mysql"
