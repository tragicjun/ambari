from resource_management import *
import os
class configinit:

  def update_config(self):
    import params

    print 'override influxdb.conf file'
    File(os.path.join(params.influxdb_config_dir,'influxdb.conf'),
      owner=params.influxdb_user,
      group=params.influxdb_group,
      mode=0664,
	  encoding='UTF-8',
      content=Template("influxdb.conf.j2")
    )

  def update_influxdb_config(self):
    self.update_config()
