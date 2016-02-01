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

import sys
import os
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils
from configinit import configinit

class Grafana_server(Script):

  def install(self, env):
    import params
    env.set_params(params)
    self.install_packages(env)

  def uninstall(self, env):
    Toolkit.uninstall_service("grafana")

  def configure(self, env):
    configinit().update_grafana_server_config()

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.initDatabase(env)
    self.configure(env)
    cmd = "({0}/bin/grafana-server -homepath {0} -pidfile {0}/pid.file web &) &>> {0}/start.log".format(params.root_dir)
    Logger.info("start grafana")
    utils().exe(cmd)

  def stop(self, env, rolling_restart=False):
    import params
    import status_params
    Logger.info("stop grafana")
    pid_file = params.root_dir + "/pid.file"
    if not pid_file or not os.path.isfile(pid_file):
      Logger.info("pid file = '{0}' is not existed".format(pid_file))
      return True
    pid = utils().exe("awk 'NR==1{print}' " + pid_file);
    utils().exe("rm -f "+pid_file)
    try:
      utils().exe("kill -9 "+pid)
    except Exception as e:
      Logger.info("kill grafana failed,pid:"+pid)
    
  def status(self, env):
    import params
    pid_file = params.root_dir + "/pid.file"
    check_process_status(pid_file)
    
  def initDatabase(self, env):
      import params
      env.set_params(params)
      File(params.init_sql_script,
           mode=0755,
           encoding='UTF-8',
           content=StaticFile('init.sql')
           )
      File(params.start_mysql_script,
           mode=0755,
           encoding='UTF-8',
           content=StaticFile('startMySql.sh')
           )
      cmd = format("bash -x {start_mysql_script} {db_host} "
                   "{db_port} {db_username} {db_password} "
                   "{db_name} {init_sql_script}")
      print cmd
      Toolkit.execute_shell(cmd,5,30)

if __name__ == "__main__":
  Grafana_server().execute()
