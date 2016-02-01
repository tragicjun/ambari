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

from webshell import webshell


class Server(Script):
  def install(self, env):
    Logger.info('install webshell server')
    import params

    excludePackage = []
    self.install_packages(env, excludePackage)

    Links(params.new_webshell_install_path, params.webshell_install_path)
    Links(params.new_webshell_conf_path, params.webshell_conf_path)

  def uninstall(self, env):
    Toolkit.uninstall_service("webshell")

  def configure(self, env):
    Logger.info('config webshell server')
    import params

    env.set_params(params)

    webshell().update_webshell_config()

  def start(self, env):
    Logger.info('start webshell server')
    import params

    env.set_params(params)

    self.configure(env)

    Toolkit.exe(params.start_server)

    Links(params.new_webshell_log_path, params.webshell_log_path)
    Links(params.new_webshell_data_path_users, params.webshell_data_path_users)
    Links(params.new_webshell_data_path_session, params.webshell_data_path_session)

  def stop(self, env):
    Logger.info('stop webshell server')
    import params

    env.set_params(params)

    Toolkit.exe(params.stop_server)
    Toolkit.kill_process(params.status_server)

  def status(self, env):
    import params
    Toolkit.check_process(params.status_server)

    # Toolkit.check_url(params.server_url, "-X GET -k")


if __name__ == "__main__":
  Server().execute()
