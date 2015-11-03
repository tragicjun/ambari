#!/usr/bin/env python

'''
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
'''

import socket
import time
import sys
import logging
import os
import subprocess
import commands

from ambari_commons import OSCheck


AMBARI_PASSPHRASE_VAR = "AMBARI_PASSPHRASE"


def execOsCommand(osCommand, tries=1, try_sleep=0):
  for i in range(0, tries):
    if i>0:
      time.sleep(try_sleep)
    
    osStat = subprocess.Popen(osCommand, stdout=subprocess.PIPE)
    log = osStat.communicate(0)
    ret = {"exitstatus": osStat.returncode, "log": log}
    
    if ret['exitstatus'] == 0:
      break
      
  return ret


def installAgent(projectVersion):
  """ Run install and make sure the agent install alright """
  # The command doesn't work with file mask ambari-agent*.rpm, so rename it on agent host
  if OSCheck.is_suse_family():
    Command = ["zypper", "--no-gpg-checks", "install", "-y", "ambari-agent-" + projectVersion]
  elif OSCheck.is_ubuntu_family():
    # add * to end of version in case of some test releases
    Command = ["apt-get", "install", "-y", "--allow-unauthenticated", "ambari-agent=" + projectVersion + "*"]
  else:
    Command = ["yum", "-y", "install", "--nogpgcheck", "ambari-agent-" + projectVersion]
  return execOsCommand(Command, tries=3, try_sleep=10)


def configureAgent(server_hostname, user_run_as):
  """ Configure the agent so that it has all the configs knobs properly installed """
  osCommand = ["sed", "-i.bak", "s/hostname=localhost/hostname=" + server_hostname +
                                "/g", "/etc/ambari-agent/conf/ambari-agent.ini"]
  ret = execOsCommand(osCommand)
  if ret['exitstatus'] != 0:
    return ret
  osCommand = ["sed", "-i.bak", "s/run_as_user=.*$/run_as_user=" + user_run_as +
                                "/g", "/etc/ambari-agent/conf/ambari-agent.ini"]
  ret = execOsCommand(osCommand)
  return ret

def runAgent(passPhrase, expected_hostname, user_run_as, verbose):
  os.environ[AMBARI_PASSPHRASE_VAR] = passPhrase
  vo = ""
  if verbose:
    vo = " -v"
  cmd = ['su', user_run_as, '-l', '-c', '/usr/sbin/ambari-agent restart --expected-hostname=%1s %2s' % (expected_hostname, vo)]
  log = ""
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  p.communicate()
  agent_retcode = p.returncode
  for i in range(3):
    time.sleep(1)
    ret = execOsCommand(["tail", "-20", "/var/log/ambari-agent/ambari-agent.log"])
    if (0 == ret['exitstatus']):
      try:
        log = ret['log']
      except Exception:
        log = "Log not found"
      print log
      break
  return {"exitstatus": agent_retcode, "log": log}
 
def tryStopAgent():
  verbose = False
  cmds = ["bash", "-c", "ps aux | grep 'AmbariAgent.py' | grep ' \-v'"]
  cmdl = ["bash", "-c", "ps aux | grep 'AmbariAgent.py' | grep ' \--verbose'"]
  if execOsCommand(cmds)["exitstatus"] == 0 or execOsCommand(cmdl)["exitstatus"] == 0:
    verbose = True
  subprocess.call("/usr/sbin/ambari-agent stop", shell=True)
  return verbose  

def getOptimalVersion(initialProjectVersion):
  optimalVersion = initialProjectVersion
  ret = findNearestAgentPackageVersion(optimalVersion)

  if ret["exitstatus"] == 0 and ret["log"][0].strip() != "" \
     and ret["log"][0].strip() == initialProjectVersion:
    optimalVersion = ret["log"][0].strip()
    retcode = 0
  else:
    ret = getAvaliableAgentPackageVersions()
    retcode = 1
    optimalVersion = ret["log"]

  return {"exitstatus": retcode, "log": optimalVersion}


def findNearestAgentPackageVersion(projectVersion):
  if projectVersion == "":
    projectVersion = "  "
  if OSCheck.is_suse_family():
    Command = ["bash", "-c", "zypper --no-gpg-checks -q search -s --match-exact ambari-agent | grep '" + projectVersion +
                                 "' | cut -d '|' -f 4 | head -n1 | sed -e 's/-\w[^:]*//1' "]
  elif OSCheck.is_ubuntu_family():
    if projectVersion == "  ":
      Command = ["bash", "-c", "apt-cache -q show ambari-agent |grep 'Version\:'|cut -d ' ' -f 2|tr -d '\\n'|sed -s 's/[-|~][A-Za-z0-9]*//'"]
    else:
      Command = ["bash", "-c", "apt-cache -q show ambari-agent |grep 'Version\:'|cut -d ' ' -f 2|grep '" +
               projectVersion + "'|tr -d '\\n'|sed -s 's/[-|~][A-Za-z0-9]*//'"]
  else:
    Command = ["bash", "-c", "yum -q list all ambari-agent | grep '" + projectVersion +
                              "' | sed -re 's/\s+/ /g' | cut -d ' ' -f 2 | head -n1 | sed -e 's/-\w[^:]*//1' "]
  return execOsCommand(Command)


def isAgentPackageAlreadyInstalled(projectVersion):
    if OSCheck.is_ubuntu_family():
      Command = ["bash", "-c", "dpkg-query -W -f='${Status} ${Version}\n' ambari-agent | grep -v deinstall | grep " + projectVersion]
    else:
      Command = ["bash", "-c", "rpm -qa | grep ambari-agent-"+projectVersion]
    ret = execOsCommand(Command)
    res = False
    if ret["exitstatus"] == 0 and ret["log"][0].strip() != "":
        res = True
    return res


def getAvaliableAgentPackageVersions():
  if OSCheck.is_suse_family():
    Command = ["bash", "-c",
        "zypper --no-gpg-checks -q search -s --match-exact ambari-agent | grep ambari-agent | sed -re 's/\s+/ /g' | cut -d '|' -f 4 | tr '\\n' ', ' | sed -s 's/[-|~][A-Za-z0-9]*//g'"]
  elif OSCheck.is_ubuntu_family():
    Command = ["bash", "-c",
        "apt-cache -q show ambari-agent|grep 'Version\:'|cut -d ' ' -f 2| tr '\\n' ', '|sed -s 's/[-|~][A-Za-z0-9]*//g'"]
  else:
    Command = ["bash", "-c",
        "yum -q list all ambari-agent | grep -E '^ambari-agent' | sed -re 's/\s+/ /g' | cut -d ' ' -f 2 | tr '\\n' ', ' | sed -s 's/[-|~][A-Za-z0-9]*//g'"]
  return execOsCommand(Command)


def checkServerReachability(host, port):
  ret = {}
  s = socket.socket()
  try:
    s.connect((host, port))
    ret = {"exitstatus": 0, "log": ""}
  except Exception:
    ret["exitstatus"] = 1
    ret["log"] = "Host registration aborted. Ambari Agent host cannot reach Ambari Server '" +\
                host+":"+str(port) + "'. " +\
                "Please check the network connectivity between the Ambari Agent host and the Ambari Server"
  return ret


#  Command line syntax help
# IsOptional  Index     Description
#               0        Expected host name
#               1        Password
#               2        Host name
#               3        User to run agent as
#      X        4        Project Version (Ambari)
#      X        5        Server port


def parseArguments(argv=None):
  if argv is None:  # make sure that arguments was passed
    return {"exitstatus": 2, "log": "No arguments were passed"}
  args = argv[1:]  # shift path to script
  if len(args) < 3:
    return {"exitstatus": 1, "log": "Not all required arguments were passed"}

  expected_hostname = args[0]
  passPhrase = args[1]
  hostname = args[2]
  user_run_as = args[3]
  projectVersion = ""
  server_port = 8080

  if len(args) > 4:
    projectVersion = args[4]

  if len(args) > 5:
    try:
      server_port = int(args[5])
    except (Exception):
      server_port = 8080

  parsed_args = (expected_hostname, passPhrase, hostname, user_run_as, projectVersion, server_port)
  return {"exitstatus": 0, "log": "", "parsed_args": parsed_args}

def configureHostname(hostName):
  if(hostName == None or hostName.strip() == ""):
    print "hostName can not be none or blank"
    return False
  #set the /etc/hosts
  # try:
  #   wHostFile=None
  #   hostFile=None
  #   try:
  #     hostsFile=file("/etc/hosts")
  #     isFirstLine = True
  #     firstLine = ""
  #     lines = []
  #     for line in hostsFile:
  #       if(isFirstLine):
  #         isFirstLine = False
  #         firstLine = line.strip()
  #       lines.append(line.strip())
  #     insertLine = "127.0.0.1 "+hostName.strip()
  #     newContent=""
  #     if(firstLine != insertLine):
  #       lines.insert(0, insertLine+"\n"+hostName.strip()+" "+hostName.strip())
  #       newContent = '\n'.join(lines)
  #
  #       wHostFile=file('/etc/hosts', 'w')
  #       wHostFile.write(newContent)
  #   finally:
  #     if(hostFile != None):
  #       hostsFile.close()
  #     if(wHostFile != None):
  #       wHostFile.close()
  # except Exception:
  #   print "errro to set /etc/hosts"
  #   traceback.print_exc()
  #   return False
  #valid the hostname
  (status, output) = commands.getstatusoutput('sudo hostname '+hostName)
  if (status != 0):
      print output
      return False
  return True

def run_setup(argv=None):
  # Parse passed arguments
  retcode = parseArguments(argv)
  if (retcode["exitstatus"] != 0):
    return retcode

  (expected_hostname, passPhrase, hostname, user_run_as, projectVersion, server_port) = retcode["parsed_args"]
  
  # configureHostname
  if(configureHostname(expected_hostname) == False):
    print "[ERROR]configure hostname failed"
  
  retcode = checkServerReachability(hostname, server_port)
  if (retcode["exitstatus"] != 0):
    return retcode

  if projectVersion == "null" or projectVersion == "{ambariVersion}" or projectVersion == "":
    retcode = getOptimalVersion("")
  else:
    retcode = getOptimalVersion(projectVersion)
  if retcode["exitstatus"] == 0 and retcode["log"] != None and retcode["log"] != "" and retcode["log"][0].strip() != "":
    availiableProjectVersion = retcode["log"].strip()
    if not isAgentPackageAlreadyInstalled(availiableProjectVersion):
      retcode = installAgent(availiableProjectVersion)
      if (not retcode["exitstatus"] == 0):
        return retcode
  elif retcode["exitstatus"] == 1 and retcode["log"][0].strip() != "":
    return {"exitstatus": 1, "log": "Desired version ("+projectVersion+") of ambari-agent package"
                                        " is not available."
                                        " Repository has following "
                                        "versions of ambari-agent:"+retcode["log"][0].strip()}
  else:
    return retcode

  retcode = configureAgent(hostname, user_run_as)
  if retcode['exitstatus'] != 0:
    return retcode
  return runAgent(passPhrase, expected_hostname, user_run_as, verbose)

def main(argv=None):
  #Try stop agent and check --verbose option if agent already run
  global verbose
  verbose = tryStopAgent()
  if verbose:
    exitcode = run_setup(argv)
  else:
    try:
      exitcode = run_setup(argv)
    except Exception, e:
      exitcode = {"exitstatus": -1, "log": str(e)}
  return exitcode

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  ret = main(sys.argv)
  retcode = ret["exitstatus"]
  if 0 != retcode:
    print ret["log"]
  sys.exit(retcode)
