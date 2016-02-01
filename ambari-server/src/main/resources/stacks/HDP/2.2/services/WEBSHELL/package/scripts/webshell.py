from resource_management import *


class webshell:
  def update_webshell_config(self):
    import params

    Logger.info('create server.conf')
    File(params.webshell_conf_path,
         mode=0755,
         content=Template("server.conf.j2")
         )

    Logger.info('create logs')
    Directory(params.server_logfile_dir,
              mode=0755
    )
