from resource_management import *
import os

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

#system
java_home = config['hostLevelParams']['java_home']
hadoop_conf_dir = "/etc/hadoop/conf"

pid_file = '/usr/local/lhotse_base/lhotsebase.pid'

#gmond
gmond_host = default("/clusterHostInfo/ganglia_server_host", ["127.0.0.1"])[0]
gmond_port = 8672

#lhotse runner config
lhotse_runner_hosts = default("/clusterHostInfo/lhotse_runner_hosts", ["127.0.0.1"])[0]
lhotse_runner_pid_file = '/usr/local/lhotse_runners/lhotserunner.pid'
config_runner_script = format("{tmp_dir}/configRunner.sh")
lhotse_runner_hadoop_env = '/etc/hadoop/conf/hadoop-env.sh'
lhotse_runner_proc_name = 'lhotse_task_loader.jar'
lhotse_runner_cgi_port = default("/configurations/lhotse-runner/cgi.port", 80)

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
lhotse_service_pid_file = '/usr/local/lhotse_services/service.pid'
service_mfs_path = default("/configurations/lhotse-service/mfs.path", '/usr/local/lhotse_services/templates')
service_config_path = '/usr/local/lhotse_services/webapps/LService/WEB-INF/classes'

# Lhotse web configurations
config_web_script = format("{tmp_dir}/configWeb.sh")
service_daemon = 'httpd'
lhotse_web_hosts = default("/clusterHostInfo/lhotse_base_hosts", ["127.0.0.1"])[0]
lhotse_web_listen_port = default("/configurations/lhotse-web/listen.port", 80)
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

#####################################################################################################################################


#config path
base_config_path = '/usr/local/lhotse_base/cfg'
runner_config_path = '/usr/local/lhotse_runners/cfg'
runner_httpd_conf_path = '/etc/httpd/conf.d'
runner_root_path = '/usr/local/lhotse_runners'
lhotse_web_root_path = '/usr/local/lhotse_web'

# Lhotse metadata database used config settings
if System.get_instance().os_family == "suse" or System.get_instance().os_family == "ubuntu":
  daemon_name = 'mysql'
else:
  daemon_name = 'mysqld'

start_mysql_script = format("{tmp_dir}/startMySql.sh")

lhotse_schema_path = format("{tmp_dir}/lhotse_schema.sql")

check_status_script = format("{tmp_dir}/checkStatus.sh")
