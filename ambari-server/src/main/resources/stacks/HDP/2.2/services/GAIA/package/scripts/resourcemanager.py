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
from resource_management import *
from resource_management.core.logger import Logger
from utils import utils
from configinit import configinit

class ResourceManager(Script):


    def install(self, env):
        import params
        Logger.info("check local host")
        utils().check_local_environment(env,params.master)

        Logger.info("install hadoop")        
        excludePackage = ['docker-ng','haproxy-ng','resource_monitor','portal_api_server']
        self.install_packages(env,excludePackage)


    def uninstall(self, env):
        Toolkit.uninstall_service("gaia")

    def configure(self, env):
        print 'configured ResourceManager'
        configinit().update_rm_configs(env)

    def start(self, env):
        import params
        env.set_params(params)

        self.configure(env)

        Logger.info("start ResourceManager")
        utils().exe(params.rm_start)

    def stop(self, env):
        import params
        Logger.info("stop ResourceManager")
        utils().exe(params.rm_stop)

    def status(self, env):
        import params
        Logger.info("status ResourceManager")
        utils().check_process(params.rm_keyword) 



if __name__ == "__main__":
    ResourceManager().execute()

