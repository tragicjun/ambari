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
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_XML
import utils  # this is needed to avoid a circular dependency since utils.py calls this class
from hdfs import hdfs
from hack_hadoop import hack_hadoop

class ZkfcSlave(Script):
  def install(self, env):
    import params

    self.install_packages(env, params.exclude_packages)
    env.set_params(params)

    # replace new hadoop jars
    hack_hadoop().hack()

  def uninstall(self, env):
    Toolkit.uninstall_service("hdfs")

  def start(self, env, rolling_restart=False):
    import params

    env.set_params(params)
    self.configure(env)
    Directory(params.hadoop_pid_dir_prefix,
              mode=0755,
              owner=params.hdfs_user,
              group=params.user_group
    )

    # format the znode for this HA setup
    # only run this format command if the active namenode hostname is set
    # The Ambari UI HA Wizard prompts the user to run this command
    # manually, so this guarantees it is only run in the Blueprints case
    if params.dfs_ha_enabled and \
       params.dfs_ha_namenode_active is not None:
      success =  initialize_ha_zookeeper(params)
      if not success:
        raise Fail("Could not initialize HA state in zookeeper")

    utils.service(
      action="start", name="zkfc", user=params.hdfs_user, create_pid_dir=True,
      create_log_dir=True
    )

  def stop(self, env, rolling_restart=False):
    import params

    env.set_params(params)
    utils.service(
      action="stop", name="zkfc", user=params.hdfs_user, create_pid_dir=True,
      create_log_dir=True
    )

  def configure(self, env):
    hdfs()
    pass

  def status(self, env):
    import status_params

    env.set_params(status_params)

    check_process_status(status_params.zkfc_pid_file)

  def security_status(self, env):
    import status_params

    env.set_params(status_params)

    props_value_check = {"hadoop.security.authentication": "kerberos",
                         "hadoop.security.authorization": "true"}
    props_empty_check = ["hadoop.security.auth_to_local"]
    props_read_check = None
    core_site_expectations = build_expectations('core-site', props_value_check, props_empty_check,
                                                props_read_check)
    hdfs_expectations = {}
    hdfs_expectations.update(core_site_expectations)

    security_params = get_params_from_filesystem(status_params.hadoop_conf_dir,
                                                   {'core-site.xml': FILE_TYPE_XML})
    result_issues = validate_security_config_properties(security_params, hdfs_expectations)
    if 'core-site' in security_params and 'hadoop.security.authentication' in security_params['core-site'] and \
        security_params['core-site']['hadoop.security.authentication'].lower() == 'kerberos':
      if not result_issues:  # If all validations passed successfully
        if status_params.hdfs_user_principal or status_params.hdfs_user_keytab:
          try:
            cached_kinit_executor(status_params.kinit_path_local,
                                  status_params.hdfs_user,
                                  status_params.hdfs_user_keytab,
                                  status_params.hdfs_user_principal,
                                  status_params.hostname,
                                  status_params.tmp_dir)
            self.put_structured_out({"securityState": "SECURED_KERBEROS"})
          except Exception as e:
            self.put_structured_out({"securityState": "ERROR"})
            self.put_structured_out({"securityStateErrorInfo": str(e)})
        else:
          self.put_structured_out(
            {"securityIssuesFound": "hdfs principal and/or keytab file is not specified"})
          self.put_structured_out({"securityState": "UNSECURED"})
      else:
        issues = []
        for cf in result_issues:
          issues.append("Configuration file %s did not pass the validation. Reason: %s" % (cf, result_issues[cf]))
        self.put_structured_out({"securityIssuesFound": ". ".join(issues)})
        self.put_structured_out({"securityState": "UNSECURED"})
    else:
      self.put_structured_out({"securityState": "UNSECURED"})

def initialize_ha_zookeeper(params):
  try:
    iterations = 10
    formatZK_cmd = "hdfs zkfc -formatZK -nonInteractive"
    Logger.info("Initialize HA state in ZooKeeper: %s" % (formatZK_cmd))
    for i in range(iterations):
      Logger.info('Try %d out of %d' % (i+1, iterations))
      code, out = shell.call(formatZK_cmd, logoutput=False, user=params.hdfs_user)
      if code == 0:
        Logger.info("HA state initialized in ZooKeeper successfully")
        return True
      elif code == 2:
        Logger.info("HA state already initialized in ZooKeeper")
        return True
      else:
        Logger.warning('HA state initialization in ZooKeeper failed with %d error code. Will retry' % (code))
  except Exception as ex:
    Logger.error('HA state initialization in ZooKeeper threw an exception. Reason %s' %(str(ex)))
  return False

if __name__ == "__main__":
  ZkfcSlave().execute()
