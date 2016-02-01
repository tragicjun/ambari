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
import json
import os

class hack_hadoop:
  def hack(self):
    # get yum repo url
    yum_repo = default("/hostLevelParams/repo_info", None)
    if not yum_repo:
      raise Fail("yum repo info not found")
    yum_repo_url = json.loads(yum_repo)[0]["defaultBaseUrl"]

    # config replacing jars
    jar_replacements = [
      ("/usr/hdp/2.2.0.0-2041/hadoop-hdfs", "hadoop-hdfs-2.6.0.jar", "hadoop-hdfs-2.6.0.2.2.0.0-2041.jar"),
      ("/usr/hdp/2.2.0.0-2041/hadoop", "hadoop-common-2.6.0.jar", "hadoop-common-2.6.0.2.2.0.0-2041.jar"),
      ("/usr/hdp/2.2.0.0-2041/hadoop-mapreduce", "hadoop-mapreduce-client-core-2.6.0.jar", "hadoop-mapreduce-client-core-2.6.0.2.2.0.0-2041.jar")
    ]

    # hack jars
    Logger.info("prepare to replace hadoop jars")
    for jar_replacement in jar_replacements:
      local_dir = jar_replacement[0]
      remote_jar_name = jar_replacement[1]
      local_jar_name = jar_replacement[2]

      # local_dir exists and hack jar anyway
      if os.path.exists(local_dir):
        remote_jar = "{0}/hadoop-2.6.0/{1}".format(yum_repo_url, remote_jar_name)
        download_jar = "{0}/{1}".format(local_dir, remote_jar_name)
        local_jar = "{0}/{1}".format(local_dir, local_jar_name)

        wget_jar_cmd = "cd {0}; wget {1} 2>/dev/null".format(local_dir, remote_jar)
        replace_jar_cmd = "mv {0} {1}".format(download_jar, local_jar)

        # download and replace
        Toolkit.exe(wget_jar_cmd)
        Toolkit.exe(replace_jar_cmd)



