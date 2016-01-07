#!/usr/bin/env bash

docker run -d --name tbds-build -w /root/tbds --entrypoint /root/tbds/build-tbds.sh -v `pwd`:/root/tbds docker.oa.com:8080/tbds/build:2.0.0-dev