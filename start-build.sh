#!/bin/bash
BUILD_DIR=`pwd`
MAVEN_REPO_HOME=/data/home/docker_common/jerryjzhang/ambari-build/m2

echo "Building $BUILD_DIR"

docker run -it --rm -v $BUILD_DIR:/ambari \
    -v $MAVEN_REPO_HOME:/root/.m2 \
    -w /ambari \
    --entrypoint /bin/bash \
    docker.oa.com:8080/tbds/build:1.0

