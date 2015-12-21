FROM docker.oa.com:8080/ambari/build:2.0.0-gaia
COPY ambari-admin /data/ambari-admin
COPY ambari-web /data/ambari-web
COPY rpm /data/rpm
RUN rpm -ivh /data/rpm/python-2.6.6-29.el6.x86_64.rpm --force
RUN rpm -e python-2.6.6-52.el6.x86_64
RUN rpm -ivh /data/rpm/python-devel-2.6.6-29.el6.x86_64.rpm