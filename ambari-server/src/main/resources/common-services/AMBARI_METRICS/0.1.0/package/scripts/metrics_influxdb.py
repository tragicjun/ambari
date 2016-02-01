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

class Influxdb(Script):
  def install(self, env):
    self.install_packages(env)
    # self.configure(env) # for security
    
    import params
    env.set_params(params)
    Links(params.new_influxdb_usr_lib, params.influxdb_usr_lib)
    Links(params.new_influxdb_var_run, params.influxdb_var_run)
    Links(params.new_influxdb_var_log, params.influxdb_var_log)
    Links(params.new_influxdb_config_dir, params.influxdb_config_dir)
    
    Links(params.new_influxdb_meta_dir, params.influxdb_meta_dir)
    Links(params.new_influxdb_data_dir, params.influxdb_data_dir)
    Links(params.new_influxdb_handoff_dir, params.influxdb_handoff_dir)

  def uninstall(self, env):
    Toolkit.uninstall_service("influxdb")

  def configure(self, env):
    import params
    env.set_params(params)
    configinit().update_influxdb_config()

  def start(self, env):
    import params
    import status_params
    env.set_params(params)
    
    self.configure(env) # for security

    cmd = "service influxdb start"
    Logger.info("start influxdb")
    utils().exe(cmd)
    check_process_status(status_params.influxdb_pid_file)

  def stop(self, env):
    import params
    env.set_params(params)
    # Sometimes, stop() may be called before start(), in case restart() is initiated right after installation
    self.configure(env) # for security
    
    cmd = "service influxdb stop"
    Logger.info("stop influxdb")
    utils().exe(cmd)

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.influxdb_pid_file)
    
if __name__ == "__main__":
  Influxdb().execute()
