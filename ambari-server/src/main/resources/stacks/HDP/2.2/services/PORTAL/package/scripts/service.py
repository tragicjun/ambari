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

from portal import portal


class Service(Script):
  def install(self, env):
    Logger.info('install portal service')
    import params
    excludePackage = []
    self.install_packages(env, excludePackage)

    Links(params.new_portal_install_path, params.portal_install_path)
    Links(params.new_portal_conf_path, params.portal_conf_path)
    Links(params.new_portal_conf_path_web, params.portal_conf_path_web)

  def uninstall(self, env):
    Toolkit.uninstall_service("portal")

  def configure(self, env):
    Logger.info('config portal service')
    import params
    env.set_params(params)

    portal().update_portal_config()

  def start(self, env):
    Logger.info('start portal service')
    import params
    env.set_params(params)

    self.configure(env)

    Toolkit.exe(params.start_service)

  def stop(self, env):
    Logger.info('stop portal service')
    import params
    env.set_params(params)

    Toolkit.exe(params.stop_service)

  def status(self, env):
    import params

    Toolkit.check_url(params.portal_service_url)


if __name__ == "__main__":
  Service().execute()
