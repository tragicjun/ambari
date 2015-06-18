from resource_management import *
import sys
import os
class configinit:

  def update_web_config(self):
    import params

    print 'create database.php'
    File(os.path.join(params.web_config_path,'database.php'),
      owner='ambari',
      group='ambari',
      mode=0644,
      content=Template("web.database.php.j2")
    )
	
  def init_mysql_scripts(self):
    import params
	
	print 'create gri_ge.sql'
    File(params.gri_ge_script,
         mode=0755,
         content=StaticFile('gri_ge.sql')
    )
	
	print 'create gri_monitor.sql'
    File(params.gri_monitor_script,
         mode=0755,
         content=StaticFile('gri_monitor.sql')
    )
	
	print 'create startMySql.sh'
    File(params.start_mysql_script,
         mode=0755,
         content=StaticFile('startMySql.sh')
    )

	print 'create configWeb.sh'
    File(params.config_web_script,
         mode=0755,
         content=StaticFile('configWeb.sh')
    )	