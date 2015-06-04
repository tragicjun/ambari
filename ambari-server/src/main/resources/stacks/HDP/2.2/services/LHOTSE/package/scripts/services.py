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
import sys
from resource_management import *
from configinit import configinit


class Services(Script):

  def install(self, env):
    import params
    
    self.install_packages(env)
    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)

    File(params.config_service_script,
         mode=0755,
         content=StaticFile('configService.sh')
    )

    cmd = format("bash -x {config_service_script} {service_java_home} {service_listen_port}")
    print cmd

    val = os.system(cmd)
    print val

    configinit().update_service_config()


  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    val = os.system("su lhotse -c '/usr/local/lhotse_services/bin/startup.sh'")
    print val

    #create pid file
    check_process = format("ls {lhotse_service_pid_file} >/dev/null 2>&1 && ps `cat {lhotse_service_pid_file}` >/dev/null 2>&1") 

    File(params.lhotse_service_pid_file,
       action="create",
       not_if=check_process,
    )


  def stop(self, env):
    import params
    env.set_params(params)

    val = os.system("su lhotse -c '/usr/local/lhotse_services/bin/shutdown.sh'")
    print val

    #delete pid file

    check_process = format("ls {lhotse_service_pid_file} >/dev/null 2>&1 && ps `cat {lhotse_service_pid_file}` >/dev/null 2>&1")
    File(params.lhotse_service_pid_file,
       action="delete",
       only_if=check_process,
    )


  def status(self, env):
    #check pid file
    import params
    var = os.path.isfile(params.lhotse_service_pid_file)
    print var

    if var:
        return 0
    else:
        print "service is not exist"
        raise ComponentIsNotRunning()


    #import params
#    env.set_params(params)

 #   val = os.system("ps -ef | grep lhotse_services | wc -l")
  #  print val
   # 
    #if val == 0:
     #   print "No lhotse services running"
      #  return 1
#    else:
 #       print "lhotse services is still running"
#
 #       return 0
     
     
    
if __name__ == "__main__":
  Services().execute()
