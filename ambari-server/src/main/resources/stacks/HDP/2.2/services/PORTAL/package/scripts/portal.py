from resource_management import *
import os


class portal:
  def update_portal_config(self):
    import params

    Logger.info('create database.php')
    File(os.path.join(params.portal_conf_path, 'database.php'),
         mode=0755,
         content=Template("database.php.j2")
         )

    Logger.info('create setting.php')
    File(os.path.join(params.portal_conf_path, 'setting.php'),
         mode=0755,
         content=Template("setting.php.j2")
         )

    Logger.info('create tbds-portal.conf')
    File(params.portal_conf_path_web,
         mode=0755,
         content=Template("tbds-portal.conf.j2")
         )
