from resource_management import *
import sys
import os
import commands
class configinit:

  def update_config(self):
    import params

    print 'create default.ini file'
    File(os.path.join(params.conf_dir,'defaults.ini'),
      owner=params.grafana_user,
      group=params.grafana_group,
      mode=0644,
      encoding='UTF-8',
      content=Template("defaults.ini.j2")
    )

  def update_grafana_server_config(self):
    self.update_config()

