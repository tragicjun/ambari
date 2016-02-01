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
from resource_management import *

from mysql import mysql


class Server(Script):
  def install(self, env):
    Logger.info('install mysql server')
    import params

    excludePackage = []
    self.install_packages(env, excludePackage)

    Links(params.new_mysql_conf_path, params.mysql_conf_path)
    Links(params.new_mysql_data_path, params.mysql_data_path)
    Links(params.new_mysql_log_path, params.mysql_log_path)

    self.start(env)
    Toolkit.exe(params.init_server)
    Toolkit.exe(params.grant_base_privilege_to_all)
    Toolkit.exe(params.grant_advanced_privilege_to_all)
    Toolkit.exe(params.grant_base_privilege_to_local)
    Toolkit.exe(params.grant_advanced_privilege_to_local)
    Toolkit.exe(params.flush_privileges)

  def uninstall(self, env):
    import params
    Toolkit.uninstall_service("mysql")
    Toolkit.exe(params.reinstall_mysql)

  def configure(self, env):
    Logger.info('config mysql server')
    import params

    env.set_params(params)

    mysql().update_mysql_config()

  def start(self, env):
    Logger.info('start mysql server')
    import params
    env.set_params(params)

    self.configure(env)

    Toolkit.exe(params.start_server)


  def stop(self, env):
    Logger.info('stop mysql server')
    import params
    env.set_params(params)

    Toolkit.exe(params.stop_server)

  def status(self, env):
    import params

    Toolkit.check_process(params.status_server)


if __name__ == "__main__":
  Server().execute()
