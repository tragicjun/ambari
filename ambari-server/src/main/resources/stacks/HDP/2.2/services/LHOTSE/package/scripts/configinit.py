from resource_management import *
import sys
import os
class configinit:

  def update_base_config(self):
    import params
    print params.base_config_path
  
    print 'create log4j.properties'
    File(os.path.join(params.base_config_path,'log4j.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.log4j.properties.j2")
    )

    print 'create lhotse.properties file'
    File(os.path.join(params.base_config_path,'lhotse.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.lhotse.properties.j2")
    )

    print 'create hadoop-metrics.properties file'
    File(os.path.join(params.base_config_path,'hadoop-metrics.properties'),
      owner='lhotse',
      group='lhotse',
      mode=0644,
      content=Template("base.hadoop-metrics.properties.j2")
    )

  def update_runner_config(self,env):
    import params
    
    print 'create configRunner.sh'
    File(params.config_runner_script,
         mode=0755,
         content=StaticFile('configRunner.sh')
    )

    print 'create hadoop-env.sh'
    var = os.path.isfile(params.lhotse_runner_hadoop_env)
    env.set_params(params)

    cmd = format("bash -x {config_runner_script} {java_home} {lhotse_runner_hosts} {lhotse_runner_cgi_port}")
    print cmd

    if var:
      res = os.system(cmd)
      print res
    else:
      print '/etc/hadoop/conf/hadoop-env.sh not exist'

    print 'create lhotse_base.properties'
    File(os.path.join(params.runner_config_path,'lhotse_base.properties'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("runner.lhotse_base.properties.j2")
    )
    
    print 'create runner.conf'
    File(os.path.join(params.runner_httpd_conf_path,'runner.conf'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("runner.httpd.settings.j2")
    )
    



  def update_service_config(self):
    import params

    print 'create system.properties'
    File(os.path.join(params.service_config_path,'system.properties'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("service.system.properties.j2")
    )

  def update_web_config(self):
    import params

    print 'create setting.php'
    File(os.path.join(params.web_config_path,'setting.php'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("web.setting.php.j2")
    )
    
    print 'create lhotse_web.conf'
    File(os.path.join(params.runner_httpd_conf_path,'lhotse_web.conf'),
      owner='hdfs',
      group='hdfs',
      mode=0644,
      content=Template("lhotse.web.httpd.settings.j2")
    )
