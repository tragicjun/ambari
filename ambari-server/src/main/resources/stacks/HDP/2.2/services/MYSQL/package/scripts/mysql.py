from resource_management import *


class mysql:

  def update_mysql_config(self):
    import params

    Logger.info('create my.cnf')
    File(params.mysql_conf_path,
         mode=0644,
         content=Template("my.cnf.j2")
         )
