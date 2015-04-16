from resource_management import *
import os

config = Script.get_config()

service_host = config['configurations']['demo-config']['host']

service_port = config['configurations']['demo-config']['port']

config_path = config['configurations']['demo-config']['config.path']

log4j_content = config['configurations']['demo-log4j']['content']
