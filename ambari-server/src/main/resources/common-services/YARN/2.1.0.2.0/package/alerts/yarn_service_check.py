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

import json
import uuid
import time
from resource_management import *

LABEL = 'Last Checkpoint: [{h} hours, {m} minutes, {tx} transactions]'

YARN_WEB_ADDRESS = '{{yarn-site/yarn.resourcemanager.webapp.address}}'
YARN_USER = '{{yarn-env/yarn_user}}'

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (YARN_WEB_ADDRESS,YARN_USER)
  
def _executeHadoop(hdfs_user, cmd, not_if=None, yes_if=None):
  hadoop_bin = "/usr/bin/hadoop"
  hadoop_conf_dir = "/etc/hadoop/conf"
  if not_if != None:
    try:
      Toolkit.execute_shell('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,not_if,hdfs_user),timeout=120)
      return True
    except Exception,e:
      print "{0} return false".format(not_if)
      
  if yes_if != None:
    Toolkit.execute_shell('su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,yes_if,hdfs_user),timeout=120)
          
  hdfs_cmd = 'su -c "{0} --config {1} {2}" - {3}'.format(hadoop_bin,hadoop_conf_dir,cmd,hdfs_user);
  return Toolkit.execute_shell(hdfs_cmd,timeout=300)

def execute(parameters=None, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label
  
  Keyword arguments:
  parameters (dictionary): a mapping of parameter key to value
  host_name (string): the name of this host where the alert is running
  """
  if parameters is None:
    return (('UNKNOWN', ['There were no parameters supplied to the script.']))
    
  web_address = "localhost:8088"
  yarn_user = "yarn"
  hdfs_user = "hdfs"
  
  if YARN_WEB_ADDRESS in parameters:
    web_address = parameters[YARN_WEB_ADDRESS]
  
  if YARN_USER in parameters:
    yarn_user = parameters[YARN_USER]
  
  # check the if yarn manager is started or not
  try:
    (ret, out) = Toolkit.execute_shell('curl "{0}/ws/v1/cluster" 2>/dev/null'.format(web_address),timeout=60)
    yarnCluster = json.loads(out)
    serviceState = yarnCluster['clusterInfo']['state']
    if serviceState.strip() != "STARTED":
      result_code = "CRITICAL"
      label = "resource manager state is not Started, state["+serviceState+"]"
      return ((result_code, [label]))
  except Exception,e:
    label = 'resource manager is down.'
    result_code = 'CRITICAL'
    return ((result_code, [label]))
    
  # check whether exists active nodeManager or not
  try:
    (ret, out) = Toolkit.execute_shell('curl "{0}/ws/v1/cluster/metrics" 2>/dev/null'.format(web_address),60)
    metrics = json.loads(out)
    activeNodeNum = metrics['clusterMetrics']['activeNodes']
    if activeNodeNum < 1:
      result_code = "CRITICAL"
      label = "there is not active nodemanager, active node number:"+str(activeNodeNum)
      return ((result_code, [label]))
  except Exception,e:
    label = 'resource manager is down.'
    result_code = 'CRITICAL'
    return ((result_code, [label]))
  
  # run the wordcount mr
  dir = '/tmp'
  service_check_input = dir+"/yarn_service_check_input"
  unique = str(uuid.uuid1()).replace("-","")
  service_check_output = dir+"/yarn_service_check_output"+unique
  
  test_dir_exists ="fs -test -e {0}".format(dir)
  create_dir_cmd = "fs -mkdir {0}".format(dir)
  
  test_input_exists ="fs -test -e {0}".format(service_check_input)
  create_input_cmd = "fs -put /etc/passwd {0}".format(service_check_input)
  
  test_output_exists ="fs -test -e {0}".format(service_check_output)
  cleanup_output_cmd = "fs -rm -r {0}".format(service_check_output)
  
  wordcount_command = "jar /usr/hdp/2.2.0.0-2041/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount {0} {1}".format(service_check_input,service_check_output)  
  
  label = 'yarn service is good'
  result_code = 'OK'
  try:
    _executeHadoop(hdfs_user, create_dir_cmd, test_dir_exists)
    _executeHadoop(hdfs_user, create_input_cmd, test_input_exists)
    _executeHadoop(hdfs_user, wordcount_command)
  except Exception,e:
    result_code = "CRITICAL"
    label = 'yarn service is down:'+str(e)
  
  _executeHadoop(hdfs_user, cleanup_output_cmd, None, test_output_exists)
  
  return ((result_code, [label]))
