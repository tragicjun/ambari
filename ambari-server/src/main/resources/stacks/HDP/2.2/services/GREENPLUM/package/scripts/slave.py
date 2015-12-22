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
import os
import subprocess

class GPSlave(Script):
  def install(self, env):
    import params
    if os.path.isfile(params.gp_install_dir + "/greenplum_path.sh"):
        return

    self.install_packages(env)
    daemon_cmd = "cd {0};unzip {1}".format(params.gp_install_dir, params.gp_install_zip)
    Execute(daemon_cmd,
          user=params.gp_user,
          )
    daemon_cmd = "ln -s {0} {1}".format(params.gp_install_dir, params.gp_install_symlink)
    Execute(daemon_cmd,
            user="root",
            )

    dataDirs = params.gp_segment_data_dir
    for dir in dataDirs.split(","):
        Directory(dir,
                  owner=params.gp_user,
                  recursive=True
                  )

    self.configure(env)

  def uninstall(self, env):
    Toolkit.uninstall_service("greenplum")

  def configure(self, env):
    import params
    env.set_params(params)

  def start(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

  def stop(self, env, rolling_restart=False):
    import params
    env.set_params(params)
    self.configure(env)

  def status(self, env):
    import status_params
    env.set_params(status_params)

    psCmd = "ps -ef|grep greenplum|grep -v grep|awk '{print $2}'"
    psProcess = subprocess.Popen(psCmd, shell=True, stdout=subprocess.PIPE)
    stdout = psProcess.communicate()[0]

    if not stdout:
        raise ComponentIsNotRunning()

if __name__ == "__main__":
    GPSlave().execute()
