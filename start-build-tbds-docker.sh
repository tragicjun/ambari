#!/usr/bin/env bash

docker run -d --name tbds-build \
       -w /root/tbds \
       --entrypoint /root/tbds/build-tbds.sh \
       -v `pwd`:/root/tbds \
       -v `pwd`/hbase.tar.gz:/root/tbds/ambari-metrics/ambari-metrics-timelineservice/target/embedded/hbase.tar.gz \
       docker.oa.com:8080/tbds/build:2.0.0-dev