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
    print "utils.py: generator gtm name " + ret
    return ret
  def get_coordinator_name(self):
    ret = "coordinator_" + self.get_local_name()
    print "utils.py: generator coordinator name " + ret
    return ret
  def get_datanode_name(self):
    ret = "datanode_" + self.get_local_name()
    print "utils.py: generator datanode name " + ret
    return ret
  def check_process(self, pid_file):
    print "check process status"
    if not pid_file or not os.path.isfile(pid_file):
      print "pid file = '" + pid_file + "' is not invalid"
      raise ComponentIsNotRunning()
    (ret, pid) = commands.getstatusoutput("awk 'NR==1{print}' " + pid_file)
    print "get pid = ", pid, ", return code = ", ret
    cmd = "ps aux | awk '{print $2}' | grep -E '^" + pid + "$' | wc -l"
    (ret, num) = commands.getstatusoutput(cmd)
    if (num == 0):
      print "process ", pid, " not exists"
      raise ComponentIsNotRunning()
    else:
      print "process ", pid, " exists"

if __name__ == "__main__":
  utils().get_local_name()
  utils().get_gtm_name()
  utils().get_coordinator_name()
  utils().get_datanode_name()
  utils().check_process("test")

