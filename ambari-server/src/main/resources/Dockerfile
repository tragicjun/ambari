FROM centos:6

RUN yum install -y wget tar
RUN wget http://10.149.27.91/hdp-mirror/ambari/ambari.repo -P /etc/yum.repos.d/
RUN yum install -y ambari-server
RUN ambari-server setup -s

CMD ambari-server start;sleep infinity
EXPOSE 8080 8440 8441