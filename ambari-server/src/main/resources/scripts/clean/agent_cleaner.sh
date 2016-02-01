#!/bin/bash
echo "[$(date "+%F %T")]"

status=$(tbds-server status | grep "not running" | wc -l)
if [[ "$status" == "1" ]]; then
  echo "server is stoped, restart it to continue ..."
  exit 0
fi

# get server ip
server='0.0.0.0'
port=$(cat /etc/tbds-server/conf/tbds.properties | grep client.api.port | cut -d '=' -f 2)
if [[ -z $port ]]; then
  port=8080
fi

user=$1
password=$2

if [[ -z "$user" || -z "$password" ]]; then
  echo "no user and password input"
  exit 1
fi

login=$(curl --user $user:$password $server:$port/api/v1 2>/dev/null | grep "Bad credentials" | wc -l)
if [[ "$login" == "1" ]]; then
  echo "bad password of admin"
  exit 1
fi

echo "----------   STOP ALL THE SERVICES   ----------"
# get cluster name
cluster=$(curl --user $user:$password http://$server:$port/api/v1/clusters 2> /dev/null | grep cluster_name | awk -F '"' '{print $4}')
started=$(curl --user $user:$password http://$server:$port/api/v1/clusters/$cluster/host_components?fields=HostRoles/state 2>/dev/null | grep -c "\"STARTED\"")
if [[ "$cluster" == "" ]]; then
  echo "no cluster exists, needn't to stop services."
elif [[ $started -gt 0 ]]; then
  echo "get cluster name = "$cluster
  echo "some components started, need to stop all the services."

  # stop all the services
  echo "send request to stop all the service"
  request=`curl -H "ContentType:application/json" -H "X-requested-By:admin" -X PUT -d '{"RequestInfo":{"context":"停止所有服务","operation_level":{"level":"CLUSTER","cluster_name":"tdw"}},"Body":{"ServiceInfo":{"state":"INSTALLED"}}}' --user $user:$password http://$server:$port/api/v1/clusters/$cluster/services?ServiceInfo/state=STARTED 2> /dev/null | grep href | awk -F '"' '{print $4}' `

  # wait services stopped
  echo "request sent ok, waiting services to be stopped ..."
  if [[ "$request" != "" ]]; then
    # wait services stopped
    times=1
    while true; do
      status=`curl --user $user:$password $request 2> /dev/null | grep request_status | awk -F '"' '{print $4}'`
      if [[ "$status" == "IN_PROGRESS" || "$status" == "PENDING" ]]; then
        echo -n \>
        sleep 5
        times=$((times+1))
        if [[ $times -eq 60 ]]; then
          echo -e "\nservices stopped timeout! please kill all the process manually."
          break
        fi
      elif [[ "$status" == "COMPLETED" ]]; then
        echo -e "\nservices stopped success !!!"
        break
      else
        echo -e "\nservices stopped failed, status = $status, please kill all the process manually."
        break
      fi
    done
  fi
else
  echo "all components not started, need not to stop all the services."
fi

echo "----------   CLEAN AGENTS ON ALL THE HOSTS  ----------"
hosts=$(curl --user $user:$password "http://$server:$port/api/v1/hosts?minimal_response=true" 2> /dev/null | grep host_name | awk -F':' '{print $2}' | sed "s/[ \"]//g")

echo "agents on following hosts will be cleaned:"
for host in $hosts; do echo $host; done

echo "begin to clean agents ..."
mkdir -p /tmp/clean
count=100
for host in $hosts
do
  /var/lib/tbds-server/resources/scripts/clean/service_cleaner ${host} &>/tmp/clean/${host}.log &
  p_num=`ps -wef | grep service_cleaner | grep -v grep -c`
  echo "${host} is cleaning..."

  while [ $p_num -ge $count ]
  do
      p_num=`ps -wef | grep service_cleaner | grep -v grep -c`
      sleep 5
  done
done

echo "waiting agents cleaning over ..."

wait

echo "[$(date "+%F %T")]"
echo "agents clean OK !"
