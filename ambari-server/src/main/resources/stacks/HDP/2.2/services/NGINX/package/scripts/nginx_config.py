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

from resource_management import *

class nginx_config:
  def generate_default(self):

    # basic functions
    get_name = lambda key: key.lower()
    get_host = lambda key: default("/clusterHostInfo/{0}".format(key.lower() + "_hosts"), None)[0]
    get_port = lambda key: default("/configurations/{0}".format(key), None)
    check_duplicated = lambda objects, getKey: len(reduce(
      lambda result, elem: result if getKey(elem) in result else result + [getKey(elem)],
      objects,
      []
    )) != len(objects)

    # get json object
    items = eval(StaticFile('map.json').get_content())

    # remove uninstalled
    items = filter(
      lambda item: default("/clusterHostInfo/{0}".format(item["host"].lower() + "_hosts"), None),
      items
    )

    # get upstream configs
    upstreams = map(
      lambda item: {
        "name": get_name(item["host"]),
        "host": get_host(item["host"]),
        "port": get_port(item["port"])
      },
      items
    )

    # add tbds-server upstream
    upstreams.append({
      "name": "tbds_server",
      "host": default("/clusterHostInfo/ambari_server_host", [None])[0],
      "port": default("/configurations/cluster-env/ambari_server_port", 8080)
    })

    # get location configs
    locations = reduce(
      lambda result, item: result + map(
        lambda key_value: {
          "name": get_name(item["host"]),
          "location": key_value[0],
          "path": key_value[1]
        },
        item["locations"].items()
      ),
      items,
      []
    )

    # set default root to tbds
    locations.append({
      "name": "tbds_server",
      "location": "/",
      "path": ""
    })

    # add tbds-server location
    locations.append({
      "name": "tbds_server",
      "location": "/tbds-server/",
      "path": "/"
    })

    # check upstream duplicated
    if check_duplicated(upstreams, lambda server: server["name"]):
      raise Fail("duplicated upstream configs in map.json")

    # check location duplicated
    if check_duplicated(locations, lambda location: location["location"]):
      raise Fail("duplicated location configs in map.json")

    return upstreams, locations


if __name__ == "__main__":
  pass
