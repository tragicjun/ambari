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
import commands
from resource_management import *

from mysql_service import mysql_service
from configinit import configinit
import web

class Web(Script):

  def install(self, env):
    import params
    
    self.install_packages(env)
    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)

    File(params.config_web_script,
         mode=0755,
         content=StaticFile('configWeb.sh')
    )

    configinit().update_web_config()
    
    cmd = format("bash -x {config_web_script} {lhotse_web_hosts} {lhotse_web_listen_port}")

    (ret, output) = commands.getstatusoutput(cmd)
    print "update web httpd------output-------"
    print output
    print ret

    if ret != 0:
        print 'update httpd config fail'
        sys.exit(1)


  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    mysql_service(daemon_name=params.service_daemon, action = 'start')

    #create pid file
    check_process = format("ls {lhotse_web_pid_file} >/dev/null 2>&1 && ps `cat {lhotse_web_pid_file}` >/dev/null 2>&1") 
    File(params.lhotse_web_pid_file,
       action="create",
       not_if=check_process,
    )

  def stop(self, env):
    import params
    env.set_params(params)
	
    #delete conf file
    cmd = format("rm {web_httpd_conf_path}/lhotse_web.conf")
    (ret, output) = commands.getstatusoutput(cmd)
    print "delete lhotse_web.conf output"
    print output
    print ret
    
    #restart httpd
    mysql_service(daemon_name=params.service_daemon, action = 'restart')

    #delete pid file
    check_process = format("ls {lhotse_web_pid_file} >/dev/null 2>&1 && ps `cat {lhotse_web_pid_file}` >/dev/null 2>&1") 
    File(params.lhotse_web_pid_file,
       action="delete",
       only_if=check_process,
    )


  def status(self, env):
    import params

    #check pid file
    var = os.path.isfile(params.lhotse_web_pid_file)
    if var:
        return 0
    else:
        print "web not exit"
        raise ComponentIsNotRunning()

    #import params
#    mysql_service(daemon_name=params.service_daemon, action = 'status')

if __name__ == "__main__":
  Web().execute()
