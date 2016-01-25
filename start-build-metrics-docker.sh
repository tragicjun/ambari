#!/usr/bin/env bash

docker run -d --name tbds-metrics-build \
       -w /root/tbds \
       --entrypoint /root/tbds/build-collector.sh \
       -v `pwd`:/root/tbds \
       docker.oa.com:8080/tbds/build:2.5.0-dev