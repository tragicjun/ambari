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
import sys
import os
def demo():
  import params
  print params.config_path
  
  print 'create log4j.properties'
  File(os.path.join(params.config_path,'log4j.properties'),
      owner='root',
      group='root',
      mode=0644,
      content=Template("demo.conf.j2")
  )

  print 'create demo_config.xml file'
  XmlConfig('demo_config.xml',
      conf_dir=params.config_path,
      configurations=params.config['configurations']['demo-config'],
      configuration_attributes=params.config['configuration_attributes']['demo-config'],
      owner='root',
      group='root'
  )

