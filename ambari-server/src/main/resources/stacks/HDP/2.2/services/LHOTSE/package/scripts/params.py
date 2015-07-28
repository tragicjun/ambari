from resource_management import *
import os

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

#system
java_home = config['hostLevelParams']['java_home']
hadoop_conf_dir = "/etc/hadoop/conf"

pid_file = '/usr/local/lhotse_base/lhotsebase.pid'

#metric
host_name = default("/hostname", "127.0.0.1")
collector_host = default("/clusterHostInfo/metrics_collector_hosts", ["127.0.0.1"])[0]
collector_port = default("/configurations/ams-site/timeline.metrics.service.webapp.address", "127.0.0.1:6188").split(":")[-1]
sink_period = default("/configurations/lhotse-base-env/metrics.report.period", 300)

#lhotse runner config
lhotse_runner_pid_file = '/usr/local/lhotse_runners/lhotserunner.pid'
config_runner_script = format("{tmp_dir}/configRunner.sh")
lhotse_runner_hadoop_env = '/etc/hadoop/conf/hadoop-env.sh'
lhotse_runner_proc_name = 'lhotse_task_loader.jar'
lhotse_runner_cgi_port = default("/configurations/lhotse-runner/cgi.port", 80)
lhotse_runner_hosts = default("/clusterHostInfo/lhotse_runner_hosts", ["127.0.0.1"])

#lhotse base config
lhotse_base_hosts = default("/clusterHostInfo/lhotse_base_hosts", ["127.0.0.1"])[0]
lhotse_base_port = default("/configurations/lhotse-base-env/lhotse.base.port", 9930)
lhotse_base_log4j_content = default("/configurations/lhotse-base-env/content", "")
lhotse_base_debug_mode = default("/configurations/lhotse-base-env/debug.mode", "true")
lhotse_base_issuer_logging_level = default("/configurations/lhotse-base-env/issuer.logging.level", "DEBUG")
lhotse_base_thrift_server_port = default("/configurations/lhotse-base-env/thrift.server.port", 8183)
lhotse_base_proc_name = 'lhotse_base.jar'


#lhotse database config
lhotse_database_hosts = default("/clusterHostInfo/lhotse_database_hosts", ["127.0.0.1"])[0]
lhotse_database_port = 3306
lhotse_database_username = default("/configurations/lhotse-database/lhotse.db.username", "lhotse")
lhotse_database_password = default("/configurations/lhotse-database/lhotse.db.password", "lhotse")
lhotse_database_data_dir = default("/configurations/lhotse-database/data.dir", "/data/mysql_data")

#lhotse service config
lhotse_service_hosts = default("/clusterHostInfo/lhotse_service_hosts", ["127.0.0.1"])[0]
config_service_script = format("{tmp_dir}/configService.sh")
service_java_home = java_home
service_listen_port = default("/configurations/lhotse-service/listen.port", 9010)
lhotse_service_pid_file = '/usr/local/lhotse_service/service.pid'
service_mfs_path = default("/configurations/lhotse-service/mfs.path", '/usr/local/lhotse_service/templates')
service_config_path = '/usr/local/lhotse_service/webapps/LService/WEB-INF/classes'
lhotse_service_proc_name = 'lhotse_service'

# Lhotse web configurations
config_web_script = format("{tmp_dir}/configWeb.sh")
service_daemon = 'httpd'
lhotse_web_hosts = default("/clusterHostInfo/lhotse_base_hosts", ["127.0.0.1"])[0]
lhotse_web_listen_port = default("/configurations/lhotse-web/listen.port", 80)
lhotse_web_url = "http://" + lhotse_web_hosts + ":" + str(lhotse_web_listen_port) + "/lhotse/index.php/"
lhotse_web_pid_file = '/usr/local/lhotse_web/web.pid'
web_config_path = '/usr/local/lhotse_web/config'

#hadoop-env.sh
hadoop_env_sh_template = config['configurations']['lhotse-hadoop-env']['content']

#ftp config
config_ftp_script = format("{tmp_dir}/configFtp.sh")
ftp_service_daemon = "vsftpd"
ftp_server_host = default("/clusterHostInfo/lhotse_ftp_hosts", ["127.0.0.1"])[0]
ftp_server_port = default("/configurations/lhotse-ftp/lhotse.ftp.port", 2121)
ftp_server_user = default("/configurations/lhotse-ftp/lhotse.ftp.user", 'root')
ftp_server_pwd = default("/configurations/lhotse-ftp/lhotse.ftp.password", '')
ftp_server_root_path = default("/configurations/lhotse-ftp/root.path", '/shell/')

#pgxz config
pg_server_host = default("/clusterHostInfo/pgxz_coordinator_hosts", ["127.0.0.1"])[0]
pg_server_port = default("/configurations/coordinator-config-env/pgxz.coordinator.port", '5434')
pg_user = default("/configurations/pgxz-global/pgxz.user", 'pgxz')
pg_password = default("/configurations/pgxz-global/pgxz.password", 'pgxz')
print "ftp server:" + ftp_server_host
#####################################################################################################################################

#hive info
hive_server_host = default("/clusterHostInfo/hive_server_host", ["127.0.0.1"])[0]
hive_server_port = default("/configurations/hive-site/hive.server2.thrift.port", '10000')
#config sql
namenode_info = default("/configurations/core-site/fs.defaultFS", 'hdfs://127.0.0.1:8020')
print namenode_info
if namenode_info.startswith('hdfs'):
    namenode_info = namenode_info[7:]
default_hdfs_host = namenode_info.split(':')[0]
print "default hdfs host:" + default_hdfs_host
default_hdfs_port = namenode_info.split(':')[1]
print "default hdfs port:" + default_hdfs_port
yarn_info = default("/configurations/yarn-site/yarn.resourcemanager.address", 'hdfs://127.0.0.1:8020')
default_yarn_host = yarn_info.split(':')[0]
default_yarn_port = yarn_info.split(':')[1]
print "default yarn host:" + default_yarn_host
print "default yarn port:" + default_yarn_port
#config path
base_config_path = '/usr/local/lhotse_base/cfg'
runner_config_path = '/usr/local/lhotse_runners/cfg'
runner_httpd_conf_path = '/etc/httpd/conf.d'
runner_root_path = '/usr/local/lhotse_runners'
lhotse_web_root_path = '/usr/local/lhotse_web'
web_httpd_conf_path = '/etc/httpd/conf.d'

# Lhotse metadata database used config settings
if System.get_instance().os_family == "suse" or System.get_instance().os_family == "ubuntu":
  daemon_name = 'mysql'
else:
  daemon_name = 'mysqld'

lhotse_schema_path = format("{tmp_dir}/lhotse_schema.sql")
start_mysql_script = format("{tmp_dir}/startMySql.sh")
check_status_script = format("{tmp_dir}/checkStatus.sh")
