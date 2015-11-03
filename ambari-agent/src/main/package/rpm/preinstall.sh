# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

STACKS_FOLDER="/var/lib/ambari-agent/cache/stacks"
STACKS_FOLDER_OLD=/var/lib/ambari-agent/cache/stacks_$(date '+%d_%m_%y_%H_%M').old

COMMON_SERVICES_FOLDER="/var/lib/ambari-agent/cache/common-services"
COMMON_SERVICES_FOLDER_OLD=/var/lib/ambari-agent/cache/common-services_$(date '+%d_%m_%y_%H_%M').old

PYTHON_LIB=$(ls /usr/lib/python*.* -d 2>/dev/null | xargs | awk '{print $1}')
if [[ -d "$PYTHON_LIB" && ! "$PYTHON_LIB" == "/usr/lib/python2.6" ]];
then
    ln -s $PYTHON_LIB /usr/lib/python2.6
fi

if [ -d "/etc/ambari-agent/conf.save" ]
then
    mv /etc/ambari-agent/conf.save /etc/ambari-agent/conf_$(date '+%d_%m_%y_%H_%M').save
fi

BAK=/etc/ambari-agent/conf/ambari-agent.ini.old
ORIG=/etc/ambari-agent/conf/ambari-agent.ini

[ -f $ORIG ] && mv -f $ORIG $BAK

if [ -d "$STACKS_FOLDER" ]
then
    mv -f "$STACKS_FOLDER" "$STACKS_FOLDER_OLD"
fi

if [ -d "$COMMON_SERVICES_FOLDER_OLD" ]
then
    mv -f "$COMMON_SERVICES_FOLDER" "$COMMON_SERVICES_FOLDER_OLD"
fi

exit 0
