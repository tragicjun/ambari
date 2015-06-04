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
from pgxz import pgxz
from utils import utils

class Datanode(Script):
  def install(self, env):
    import params
    self.install_packages(env)
    print 'init datanode'
    #su pgxz -c '/usr/local/pgxz/bin/initdb -D /usr/local/pgxz/nodes/datanode --nodename datanode'
    print params.datanode_install
    val= os.system(params.datanode_install)
    print val

  def start(self, env):
    import params
    print 'create datanode config'
    self.configure(env)

    print 'start datanode'
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl start -D /usr/local/pgxz/nodes/datanode -Z datanode'
    print params.datanode_start
    val= os.system(params.datanode_start)
    print val


  def configure(self, env):
    import params
    print 'create the config file by pgxz().init_datanode()';
    env.set_params(params)
    pgxz().init_datanode()

  def stop(self, env):
    import params
    print 'Stop the datanode';
    #su pgxz -c '/usr/local/pgxz/bin/pg_ctl stop -D /usr/local/pgxz/nodes/datanode -Z datanode'
    print params.datanode_stop
    val= os.system(params.datanode_stop)
    print val
     
  def status(self, env):
    import params
    print 'Status of the datanode';
    utils().check_process(params.datanode_pid)

if __name__ == "__main__":
  Datanode().execute()
