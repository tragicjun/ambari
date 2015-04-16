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

