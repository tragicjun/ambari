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

from functions import calc_xmn_from_xms
from resource_management import *
import status_params
from ambari_commons import OSCheck

if OSCheck.is_windows_family():
  from params_windows import *
else:
  from params_linux import *
# server configurations
config = Script.get_config()
exec_tmp_dir = Script.get_tmp_dir()

#AMBARI_METRICS data
ams_pid_dir = status_params.ams_collector_pid_dir

ams_collector_script = "/usr/sbin/ambari-metrics-collector"
ams_collector_pid_dir = status_params.ams_collector_pid_dir
ams_collector_hosts = default("/clusterHostInfo/metrics_collector_hosts", [])
ams_collector_host_single = ams_collector_hosts[0] #TODO cardinality is 1+ so we can have more than one host
metric_collector_port = default("/configurations/ams-site/timeline.metrics.service.webapp.address", "0.0.0.0:6188")
if metric_collector_port and metric_collector_port.find(':') != -1:
  metric_collector_port = metric_collector_port.split(':')[1]
pass

ams_collector_log_dir = config['configurations']['ams-env']['metrics_collector_log_dir']
ams_monitor_log_dir = config['configurations']['ams-env']['metrics_monitor_log_dir']

ams_monitor_dir = "/usr/lib/python2.6/site-packages/resource_monitoring"
ams_monitor_pid_dir = status_params.ams_monitor_pid_dir
ams_monitor_script = "/usr/sbin/ambari-metrics-monitor"

ams_hbase_home_dir = "/usr/lib/ams-hbase/"

#hadoop params

hbase_excluded_hosts = config['commandParams']['excluded_hosts']
hbase_drain_only = config['commandParams']['mark_draining_only']
hbase_included_hosts = config['commandParams']['included_hosts']

hbase_user = status_params.hbase_user
smokeuser = config['configurations']['cluster-env']['smokeuser']
hbase_root_dir = config['configurations']['ams-hbase-site']['hbase.rootdir']

is_hbase_distributed = hbase_root_dir.startswith('hdfs://')

# security is disabled for embedded mode, when HBase is backed by file
security_enabled = False if not is_hbase_distributed else config['configurations']['cluster-env']['security_enabled']

# this is "hadoop-metrics.properties" for 1.x stacks
metric_prop_file_name = "hadoop-metrics2-hbase.properties"

# not supporting 32 bit jdk.
java64_home = config['hostLevelParams']['java_home']

metrics_collector_heapsize = default('/configurations/ams-env/metrics_collector_heapsize', "512m")

hbase_log_dir = config['configurations']['ams-hbase-env']['hbase_log_dir']
master_heapsize = config['configurations']['ams-hbase-env']['hbase_master_heapsize']
regionserver_heapsize = config['configurations']['ams-hbase-env']['hbase_regionserver_heapsize']

regionserver_xmn_max = default('configurations/ams-hbase-env/hbase_regionserver_xmn_max', None)
if regionserver_xmn_max:
  regionserver_xmn_percent = config['configurations']['ams-hbase-env']['hbase_regionserver_xmn_ratio']
  regionserver_xmn_size = calc_xmn_from_xms(regionserver_heapsize, regionserver_xmn_percent, regionserver_xmn_max)
else:
  regionserver_xmn_size = config['configurations']['ams-hbase-env']['regionserver_xmn_size']
pass
# For embedded mode
hbase_heapsize = master_heapsize
hbase_master_xmn_size = config['configurations']['ams-hbase-env']['hbase_master_xmn_size']
hbase_master_maxperm_size = config['configurations']['ams-hbase-env']['hbase_master_maxperm_size']

zookeeper_quorum_hosts = ','.join(ams_collector_hosts) if is_hbase_distributed else 'localhost'

ams_checkpoint_dir = config['configurations']['ams-site']['timeline.metrics.aggregator.checkpoint.dir']
hbase_pid_dir = status_params.hbase_pid_dir
hbase_tmp_dir = config['configurations']['ams-hbase-site']['hbase.tmp.dir']
# TODO UPGRADE default, update site during upgrade
_local_dir_conf = default('/configurations/ams-hbase-site/hbase.local.dir', "${hbase.tmp.dir}/local")
local_dir = substitute_vars(_local_dir_conf, config['configurations']['ams-hbase-site'])

phoenix_max_global_mem_percent = default('/configurations/ams-site/phoenix.query.maxGlobalMemoryPercentage', '20')
phoenix_client_spool_dir = default('/configurations/ams-site/phoenix.spool.directory', '/tmp')
phoenix_server_spool_dir = default('/configurations/ams-hbase-site/phoenix.spool.directory', '/tmp')
# Substitute vars if present
phoenix_client_spool_dir = substitute_vars(phoenix_client_spool_dir, config['configurations']['ams-hbase-site'])
phoenix_server_spool_dir = substitute_vars(phoenix_server_spool_dir, config['configurations']['ams-hbase-site'])

client_jaas_config_file = format("{hbase_conf_dir}/hbase_client_jaas.conf")
master_jaas_config_file = format("{hbase_conf_dir}/hbase_master_jaas.conf")
regionserver_jaas_config_file = format("{hbase_conf_dir}/hbase_regionserver_jaas.conf")

rs_hosts = ["localhost"]

smoke_test_user = config['configurations']['cluster-env']['smokeuser']
smokeuser_permissions = "RWXCA"
service_check_data = functions.get_unique_id_and_date()
user_group = config['configurations']['cluster-env']["user_group"]
hadoop_user = "hadoop"

kinit_cmd = ""

if security_enabled:
  _hostname_lowercase = config['hostname'].lower()
  client_jaas_config_file = format("{hbase_conf_dir}/hbase_client_jaas.conf")
  smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
  hbase_user_keytab = config['configurations']['ams-hbase-env']['hbase_user_keytab']

  ams_collector_jaas_config_file = format("{hbase_conf_dir}/ams_collector_jaas.conf")
  ams_collector_keytab_path = config['configurations']['ams-hbase-security-site']['hbase.myclient.keytab']
  ams_collector_jaas_princ = config['configurations']['ams-hbase-security-site']['hbase.myclient.principal'].replace('_HOST',_hostname_lowercase)

  ams_zookeeper_jaas_config_file = format("{hbase_conf_dir}/ams_zookeeper_jaas.conf")
  ams_zookeeper_keytab = config['configurations']['ams-hbase-security-site']['ams.zookeeper.keytab']
  ams_zookeeper_principal_name = config['configurations']['ams-hbase-security-site']['ams.zookeeper.principal'].replace('_HOST',_hostname_lowercase)

  master_jaas_config_file = format("{hbase_conf_dir}/hbase_master_jaas.conf")
  master_keytab_path = config['configurations']['ams-hbase-security-site']['hbase.master.keytab.file']
  master_jaas_princ = config['configurations']['ams-hbase-security-site']['hbase.master.kerberos.principal'].replace('_HOST',_hostname_lowercase)

  regionserver_jaas_config_file = format("{hbase_conf_dir}/hbase_regionserver_jaas.conf")
  regionserver_keytab_path = config['configurations']['ams-hbase-security-site']['hbase.regionserver.keytab.file']
  regionserver_jaas_princ = config['configurations']['ams-hbase-security-site']['hbase.regionserver.kerberos.principal'].replace('_HOST',_hostname_lowercase)

#log4j.properties
if (('ams-hbase-log4j' in config['configurations']) and ('content' in config['configurations']['ams-hbase-log4j'])):
  hbase_log4j_props = config['configurations']['ams-hbase-log4j']['content']
else:
  hbase_log4j_props = None

if (('ams-log4j' in config['configurations']) and ('content' in config['configurations']['ams-log4j'])):
  log4j_props = config['configurations']['ams-log4j']['content']
else:
  log4j_props = None

hbase_env_sh_template = config['configurations']['ams-hbase-env']['content']
ams_env_sh_template = config['configurations']['ams-env']['content']


hbase_staging_dir = "/apps/hbase/staging"
#for create_hdfs_directory
hostname = config["hostname"]
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
kinit_path_local = functions.get_kinit_path()

import functools
# create partial functions with common arguments for every HdfsDirectory call
# to create hdfs directory we need to call params.HdfsDirectory in code
HdfsDirectory = functools.partial(
  HdfsDirectory,
  conf_dir=hadoop_conf_dir,
  hdfs_user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  bin_dir = hadoop_bin_dir
)

# refractor service path
metrics_install_path_collector_bin = "/usr/sbin/ambari-metrics-collector"
metrics_install_path_collector_lib = "/usr/lib/ambari-metrics-collector"
metrics_install_path_monitor_bin = "/usr/sbin/ambari-metrics-monitor"
metrics_install_path_monitor_lib = "/usr/lib/python2.6/site-packages/resource_monitoring"

metrics_config_path_collector = "/etc/ambari-metrics-collector/conf"
metrics_config_path_hbase = "/etc/ams-hbase/conf"
metrics_config_path_monitor = "/etc/ambari-metrics-monitor/conf"

metrics_log_path_collector = default("/configurations/ams-env/metrics_collector_log_dir", "/data/var/log/ambari-metrics-collector")
metrics_log_path_hbase = default("/configurations/ams-hbase-env/hbase_log_dir", "/data/var/log/ambari-metrics-collector")
metrics_log_path_monitor = default("/configurations/ams-env/metrics_monitor_log_dir", "/data/var/log/ambari-metrics-monitor")

metrics_data_path_collector_hbase = default("/configurations/ams-hbase-site/hbase.rootdir", "file:///data/var/lib/ambari-metrics-collector/hbase").split("//")[-1]
metrics_data_path_collector_checkpoint = default("/configurations/ams-site/timeline.metrics.aggregator.checkpoint.dir", "/data/var/lib/ambari-metrics-collector/checkpoint")
metrics_data_path_collector_hbasetmp = default("/configurations/ams-hbase-site/hbase.tmp.dir", "/data/var/lib/ambari-metrics-collector/hbase-tmp")

new_metrics_install_path_collector_bin = "/opt/tbds/metrics/collector/ambari-metrics-collector"
new_metrics_install_path_collector_lib = "/opt/tbds/metrics/collector/lib"
new_metrics_install_path_monitor_bin = "/opt/tbds/metrics/monitor/ambari-metrics-monitor"
new_metrics_install_path_monitor_lib = "/opt/tbds/metrics/monitor/lib"

new_metrics_config_path_collector = "/etc/tbds/metrics/collector/collector"
new_metrics_config_path_hbase = "/etc/tbds/metrics/collector/hbase"
new_metrics_config_path_monitor = "/etc/tbds/metrics/monitor"

new_metrics_log_path_collector = "/var/log/tbds/metrics/collector/collector"
new_metrics_log_path_hbase = "/var/log/tbds/metrics/collector/hbase"
new_metrics_log_path_monitor = "/var/log/tbds/metrics/monitor"

new_metrics_data_path_collector_hbase = "/data/tbds/metrics/hbase"
new_metrics_data_path_collector_checkpoint = "/data/tbds/metrics/checkpoint"
new_metrics_data_path_collector_hbasetmp = "/data/tbds/metrics/hbase-tmp"


