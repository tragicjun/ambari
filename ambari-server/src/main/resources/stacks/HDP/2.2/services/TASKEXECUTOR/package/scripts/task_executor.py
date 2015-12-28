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
import os
from ambari_commons import OSConst
from resource_management import *
from resource_management.core.logger import Logger
import sys


class taskExecutor(Script):


    def install(self, env):
        self.install_packages(env)
        print 'installed task executor'


    def configure(self, env):
        import params
        Logger.info('create application.properties.j2')

        File(os.path.join(params.config_path,'application.properties'),
           mode=0644,
           content=Template("application.properties.j2")
        )

    def start(self, env):
        import os
        import params
        env.set_params(params)
        self.configure(env)
        res=Toolkit.exe(params.start_cmd)
        print res

    def stop(self, env):
        import os
        import params
        res = Toolkit.exe(params.stop_cmd)
        print res

    def status(self, env):
        import os.path
        import params
        res = Toolkit.exe(params.status_cmd)

        if res.find('is running') < 0:
            raise ComponentIsNotRunning()
        pass



if __name__ == "__main__":
    taskExecutor().execute()
