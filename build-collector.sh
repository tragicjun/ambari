#!/bin/bash

distVersion=2.4.0.0
rpmVersion=2.4.0-0
svnURL=http://tc-svn.tencent.com/doss/doss_tbds_rep/tbds_proj/trunk/tbds

#svn co $svnURL
ln -s /root/hbase.tar.gz /root/tbds/ambari-metrics/ambari-metrics-timelineservice/target/embedded/hbase.tar.gz
ln -s /root/hadoop.tar.gz /root/tbds/ambari-metrics/ambari-metrics-assembly/target/embedded/hadoop.tar.gz

for i in `find /root/tbds/ambari-metrics -type f -name "*tbds*" -or -name "*ambari*" -or -name "*.py" -or -name "*.json" -or -name "*.xml" -or -name "*.sh" -or -name "*.java" |grep -v .git | grep -v target |grep -v jar|grep -v png`;do dos2unix $i; done

mvn versions:set -DnewVersion=$distVersion -o
pushd ambari-metrics
mvn versions:set -DnewVersion=$distVersion -o
mvn install package rpm:rpm -o -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion
popd

mv ambari-metrics/ambari-metrics-timelineservice/target/rpm/ambari-metrics-collector/RPMS/noarch/ambari-metrics-collector-$rpmVersion.noarch.rpm .