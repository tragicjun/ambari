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

Ambari Agent

"""

import os
import tempfile
from resource_management.core import shell
from resource_management.core.logger import Logger
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# os.chown replacement
def chown(path, owner, group):
  if owner:
    shell.checked_call(["chown", owner, path], sudo=True)
  if group:
    shell.checked_call(["chgrp", group, path], sudo=True)
    
# os.chmod replacement
def chmod(path, mode):
  shell.checked_call(["chmod", oct(mode), path], sudo=True)
  
def chmod_extended(path, mode):
  shell.checked_call(["chmod", mode, path], sudo=True)
  
# os.makedirs replacement
def makedirs(path, mode):
  shell.checked_call(["mkdir", "-p", path], sudo=True)
  chmod(path, mode)
  
# os.makedir replacement
def makedir(path, mode):
  shell.checked_call(["mkdir", path], sudo=True)
  chmod(path, mode)
  
# os.symlink replacement
def symlink(source, link_name):
  shell.checked_call(["ln","-sf", source, link_name], sudo=True)
  
# os.link replacement
def link(source, link_name):
  shell.checked_call(["ln", "-f", source, link_name], sudo=True)
  
# os unlink
def unlink(path):
  shell.checked_call(["rm","-f", path], sudo=True)
  
# shutil.rmtree
def rmtree(path):
  shell.checked_call(["rm","-rf", path], sudo=True)
  
# fp.write replacement
def create_file(filename, content):
  """
  if content is None, create empty file
  """
  tmpf = tempfile.NamedTemporaryFile()
  
  if content:
    with open(tmpf.name, "wb") as fp:
      fp.write(content)
  
  with tmpf:    
    shell.checked_call(["cp", "-f", tmpf.name, filename], sudo=True)
    
  # set default files mode
  chmod(filename, 0644)
    
# fp.read replacement
def read_file(filename):
  tmpf = tempfile.NamedTemporaryFile()
  shell.checked_call(["cp", "-f", filename, tmpf.name], sudo=True)
  
  with tmpf:
    with open(tmpf.name, "rb") as fp:
      return fp.read()
    
# os.path.exists
def path_exists(path):
  return (shell.call(["test", "-e", path], sudo=True)[0] == 0)

# os.path.isdir
def path_isdir(path):
  return (shell.call(["test", "-d", path], sudo=True)[0] == 0)

# os.path.lexists
def path_lexists(path):
  return (shell.call(["test", "-L", path], sudo=True)[0] == 0)

# os.stat
def stat(path):
  class Stat:
    RETRY_COUNT = 5
    def __init__(self, path):
      # Sometimes (on heavy load) stat call returns an empty output with zero return code
      for i in range(0, self.RETRY_COUNT):
        out = shell.checked_call(["stat", "-c", "%u %g %a", path], sudo=True)[1]
        values = out.split(' ')
        if len(values) == 3:
          uid_str, gid_str, mode_str = values
          self.st_uid, self.st_gid, self.st_mode = int(uid_str), int(gid_str), int(mode_str, 8)
          break
      else:
        warning_message = "Can not parse a sudo stat call output: \"{0}\"".format(out)
        Logger.warning(warning_message)
        stat_val = os.stat(path)
        self.st_uid, self.st_gid, self.st_mode = stat_val.st_uid, stat_val.st_gid, stat_val.st_mode & 07777
  return Stat(path)
