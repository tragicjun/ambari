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

import falcon_server_upgrade

from resource_management import *
from resource_management.libraries.functions.version import *
from resource_management.libraries.functions.security_commons import build_expectations, \
  cached_kinit_executor, get_params_from_filesystem, validate_security_config_properties, \
  FILE_TYPE_PROPERTIES
from falcon import falcon

class FalconServer(Script):

  def get_stack_to_component(self):
    return {"HDP": "falcon-server"}

  def install(self, env):
    import params

    self.install_packages(env)
    env.set_params(params)

  def uninstall(self, env):
    Toolkit.uninstall_service("falcon")

  def start(self, env, rolling_restart=False):
    import params

    env.set_params(params)
    self.configure(env)

    falcon('server', action='start')


  def stop(self, env, rolling_restart=False):
    import params

    env.set_params(params)

    falcon('server', action='stop')

    # if performing an upgrade, backup some directories after stopping falcon
    if rolling_restart:
      falcon_server_upgrade.post_stop_backup()


  def configure(self, env):
    import params

    env.set_params(params)

    falcon('server', action='config')


  def status(self, env):
    import status_params

    env.set_params(status_params)
    check_process_status(status_params.server_pid_file)


  def pre_rolling_restart(self, env):
    import params
    env.set_params(params)

    # this function should not execute if the version can't be determined or
    # is not at least HDP 2.2.0.0
    if not params.version or compare_versions(format_hdp_stack_version(params.version), '2.2.0.0') < 0:
      return

    Logger.info("Executing Falcon Server Rolling Upgrade pre-restart")
    Execute(format("hdp-select set falcon-server {version}"))
    falcon_server_upgrade.pre_start_restore()

  def security_status(self, env):
    import status_params
    env.set_params(status_params)
    if status_params.security_enabled:
      props_value_check = {"*.falcon.authentication.type": "kerberos",
                           "*.falcon.http.authentication.type": "kerberos"}
      props_empty_check = ["*.falcon.service.authentication.kerberos.principal",
                           "*.falcon.service.authentication.kerberos.keytab",
                           "*.falcon.http.authentication.kerberos.principal",
                           "*.falcon.http.authentication.kerberos.keytab"]
      props_read_check = ["*.falcon.service.authentication.kerberos.keytab",
                          "*.falcon.http.authentication.kerberos.keytab"]
      falcon_startup_props = build_expectations('startup', props_value_check, props_empty_check,
                                                  props_read_check)

      falcon_expectations ={}
      falcon_expectations.update(falcon_startup_props)

      security_params = get_params_from_filesystem('/etc/falcon/conf',
                                                   {'startup.properties': FILE_TYPE_PROPERTIES})
      result_issues = validate_security_config_properties(security_params, falcon_expectations)
      if not result_issues: # If all validations passed successfully
        try:
          # Double check the dict before calling execute
          if ( 'startup' not in security_params
               or '*.falcon.service.authentication.kerberos.keytab' not in security_params['startup']
               or '*.falcon.service.authentication.kerberos.principal' not in security_params['startup']) \
            or '*.falcon.http.authentication.kerberos.keytab' not in security_params['startup'] \
            or '*.falcon.http.authentication.kerberos.principal' not in security_params['startup']:
            self.put_structured_out({"securityState": "UNSECURED"})
            self.put_structured_out(
              {"securityIssuesFound": "Keytab file or principal are not set property."})
            return

          cached_kinit_executor(status_params.kinit_path_local,
                                status_params.falcon_user,
                                security_params['startup']['*.falcon.service.authentication.kerberos.keytab'],
                                security_params['startup']['*.falcon.service.authentication.kerberos.principal'],
                                status_params.hostname,
                                status_params.tmp_dir)
          cached_kinit_executor(status_params.kinit_path_local,
                                status_params.falcon_user,
                                security_params['startup']['*.falcon.http.authentication.kerberos.keytab'],
                                security_params['startup']['*.falcon.http.authentication.kerberos.principal'],
                                status_params.hostname,
                                status_params.tmp_dir)
          self.put_structured_out({"securityState": "SECURED_KERBEROS"})
        except Exception as e:
          self.put_structured_out({"securityState": "ERROR"})
          self.put_structured_out({"securityStateErrorInfo": str(e)})
      else:
        issues = []
        for cf in result_issues:
          issues.append("Configuration file %s did not pass the validation. Reason: %s" % (cf, result_issues[cf]))
        self.put_structured_out({"securityIssuesFound": ". ".join(issues)})
        self.put_structured_out({"securityState": "UNSECURED"})
    else:
      self.put_structured_out({"securityState": "UNSECURED"})


if __name__ == "__main__":
  FalconServer().execute()
