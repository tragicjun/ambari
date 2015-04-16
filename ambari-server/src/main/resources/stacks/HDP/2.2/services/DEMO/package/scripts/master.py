import sys
import os
from resource_management import *
from demo import demo

class Master(Script):
  def install(self, env):
    self.install_packages(env)

  def start(self, env):
    print 'start the helloworld';
    val= os.system("/usr/bin/helloworld")
    print val
    print 'call self.config'
    self.configure(env)


  def configure(self, env):
    print 'create the config file call demo()';
    import params
    env.set_params(params)
    demo()
  def stop(self, env):
    print 'Stop the helloworld';
     
  def status(self, env):
    print 'Status of the Sample Srv Master';

if __name__ == "__main__":
  Master().execute()

