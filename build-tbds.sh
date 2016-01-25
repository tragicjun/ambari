#!/bin/bash

distVersion=2.4.0.0
rpmVersion=2.4.0-0
svnURL=http://tc-svn.tencent.com/doss/doss_tbds_rep/tbds_proj/trunk/tbds

#svn co $svnURL

rm -r /root/tbds/ambari-web/node_modules
rm -r /root/tbds/ambari-admin/src/main/resources/ui/admin-web/node_modules
rm -r /root/tbds/ambari-admin/src/main/resources/ui/admin-web/node
ln -s /root/ambari-web/node_modules /root/tbds/ambari-web/node_modules
ln -s /root/ambari-admin/node_modules /root/tbds/ambari-admin/src/main/resources/ui/admin-web/node_modules
ln -s /root/ambari-admin/node /root/tbds/ambari-admin/src/main/resources/ui/admin-web/node
ln -s /root/ambari-admin/target /root/tbds/ambari-admin/target

for i in `find /root/tbds -type f -name "*tbds*" -or -name "*ambari*" -or -name "*.py" -or -name "*.json" -or -name "*.xml" -or -name "*.sh" -or -name "*.java" |grep -v .git | grep -v target |grep -v jar|grep -v png`;do dos2unix $i; done

mkdir -p /root/tbds/ambari-agent/target/ambari-agent-$distVersion/
mkdir -p /root/tbds/ambari-client/python-client/target/python-client-$distVersion/
mkdir -p /root/tbds/ambari-shell/ambari-python-shell/target/ambari-python-shell-$distVersion/
cp -r /root/tbds/ambari-agent/src/main/python/ambari_agent/  /root/tbds/ambari-agent/target/ambari-agent-$distVersion/
cp -r /root/tbds/ambari-client/python-client/src/main/python/ambari_client /root/tbds/ambari-client/python-client/target/python-client-$distVersion/
cp -r /root/tbds/ambari-shell/ambari-python-shell/src/main/python/ambari_shell /root/tbds/ambari-shell/ambari-python-shell/target/ambari-python-shell-$distVersion/

chmod +x /root/tbds/ambari-agent/../ambari-common/src/main/unix/ambari-python-wrap

mvn versions:set -DnewVersion=$distVersion -o
pushd ambari-metrics
mvn versions:set -DnewVersion=$distVersion -o
mvn install package rpm:rpm -o -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion
popd

mvn install package rpm:rpm -o -pl '!ambari-admin' -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -DskipAssembly -DnewVersion=$distVersion -Dpython.ver="python >= 2.6"

#svn delete tbds-server-$rpmVersion.noarch.rpm ambari-agent-$rpmVersion.x86_64.rpm
mv ambari-server/target/rpm/tbds-server/RPMS/x86_64/tbds-server-$rpmVersion.x86_64.rpm .
mv ambari-agent/target/rpm/ambari-agent/RPMS/x86_64/ambari-agent-$rpmVersion.x86_64.rpm .

#svn add tbds-server-$rpmVersion.noarch.rpm ambari-agent-$rpmVersion.x86_64.rpm
#svn commit -m 'new rpms' tbds-server-$rpmVersion.noarch.rpm ambari-agent-$rpmVersion.x86_64.rpm