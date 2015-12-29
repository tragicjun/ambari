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

import json
from resource_management import *
config = Script.get_config()

class nginx_config:

  def generate_default(self):
    jsonStr = """{
    "resultCode": "0",
    "message": null,
    "resultData": [
      {
        "componentName": "GOLDENEYE_WEB",
        "configKey": "listen.port",
        "configName": "goldeneye-web",
        "ngxPath": "/ge",
        "serviceName": "GOLDENEYE",
        "servicePath": "/ge"
      },
      {
        "componentName": "NIFI_SERVER",
        "configKey": "nifi.http.port",
        "configName": "nifi-site",
        "ngxPath": "/nifi",
        "serviceName": "NIFI",
        "servicePath": "/nifi"
      },
      {
        "componentName": "LHOTSE_WEB",
        "configKey": "listen.port",
        "configName": "lhotse-web",
        "ngxPath": "/lhotse",
        "serviceName": "LHOTSE",
        "servicePath": "/lhotse"
      },
      {
        "componentName": "HUE_SERVER",
        "configKey": "http.port",
        "configName": "hue-site",
        "ngxPath": "/beeswax",
        "serviceName": "HUE",
        "servicePath": "/beeswax",
        "suffix": "/"
      },
      {
        "componentName": "HUE_SERVER",
        "configKey": "http.port",
        "configName": "hue-site",
        "ngxPath": "/spark",
        "serviceName": "HUE",
        "servicePath": "/spark",
        "suffix": "/"
      },
      {
        "componentName": "HUE_SERVER",
        "configKey": "http.port",
        "configName": "hue-site",
        "ngxPath": "/filebrowser",
        "serviceName": "HUE",
        "servicePath": "/filebrowser",
        "suffix": "/"
      },
      {
        "componentName": "HUE_SERVER",
        "configKey": "http.port",
        "configName": "hue-site",
        "ngxPath": "/metastore",
        "serviceName": "HUE",
        "servicePath": "/metastore",
        "suffix": "/"
      }
    ]
  }"""

    locations = map(
      lambda item:
      {
        "name": item["componentName"].lower(),
        "host": default("/clusterHostInfo/{0}".format(item["componentName"].lower() + "_hosts"), None)[0],
        "port": default("/configurations/{0}/{1}".format(item["configName"], item["configKey"]), None),
        "location": item["ngxPath"],
        "path": item["servicePath"]
      },
      filter(
        lambda item: default("/clusterHostInfo/{0}".format(item["componentName"].lower() + "_hosts"), None),
        json.loads(jsonStr)["resultData"]
      )
    )

    servers = reduce(
      lambda uniq, item: uniq if item["name"] in map(
        lambda uniq_item: uniq_item["name"],
        uniq
      ) else uniq + [item],
      [[], ] + locations
    )

    return servers, locations

if __name__ == "__main__":
    print nginx_config().generate_default()
