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
import commands
import socket
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger  
import time

class utils:
  def get_local_ip(self):
    localip = socket.gethostbyname(socket.gethostname())
    return localip

  def get_local_name(self):
    localip = self.get_local_ip()
    localname = localip.replace(".", "_")
    return localname

  def get_gtm_name(self):
    ret = "gtm_" + self.get_local_name()
    Logger.info("utils.py: generator gtm name {0}".format(ret))
    return ret

  def get_coordinator_name(self):
    ret = "coordinator_" + self.get_local_name()
    Logger.info("utils.py: generator coordinator name {0}".format(ret))
    return ret
  
  def get_datanode_name(self):
    ret = "datanode_" + self.get_local_name()
    Logger.info("utils.py: generator datanode name {0}".format(ret))
    return ret
  
  def exe(self, cmd):
    Logger.info("exec command: {0}".format(cmd))
    #(status, output) = commands.getstatusoutput(cmd)
    status = os.system(cmd)
    if (status != 0):
      Logger.error("command exec error, return code = {0}".format(status))
      #raise Fail()
    #Logger.info(output)

  def check_process(self, pid_file):
    Logger.info("check process status")
    if not pid_file or not os.path.isfile(pid_file):
      Logger.info("pid file = '{0}' is not existed".format(pid_file))
      raise ComponentIsNotRunning()
    (ret, pid) = commands.getstatusoutput("awk 'NR==1{print}' " + pid_file)
    Logger.info("get pid = {0}, return code = {1}".format(pid, ret))
    cmd = "ps aux | awk '{print $2}' | grep -E '^" + pid + "$' | wc -l"
    (ret, num) = commands.getstatusoutput(cmd)
    if (num == 0):
      Logger.info("process {0} not exists".format(pid))
      raise ComponentIsNotRunning()
    else:
      Logger.info("process {0} exists".format(pid))

  def check_install(self, node_dir):
    Logger.info("checking path {0}".format(node_dir));
    if not os.path.isdir(node_dir):
      Logger.error("path {0} init failed".format(node_dir));
      raise Fail()
    Logger.info("path {0} init success".format(node_dir));

  def check_start(self, pid_file):
    Logger.info("check whether process start")
    time.sleep(1)
    try:
      self.check_process(pid_file)
    except ComponentIsNotRunning:
      Logger.error("process start failed")
      raise Fail()
    Logger.info("process start success")

  def check_stop(self, pid_file):
    Logger.info("check whether process stop")
    try:
      self.check_process(pid_file)
    except ComponentIsNotRunning:
      Logger.info("process stop success")
      return
    Logger.error("process stop failed")
    raise Fail()

if __name__ == "__main__":
  utils().exe("pwd")
  utils().get_local_name()
  utils().get_gtm_name()
  utils().get_coordinator_name()
  utils().get_datanode_name()
  utils().check_install("/")
  utils().check_stop("test")
  utils().check_start("test")

