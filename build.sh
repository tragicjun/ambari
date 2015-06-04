#!/bin/sh

mvn install rpm:rpm -Dfindbugs.skip -DskipTests -Drat.skip -Dmaven.test.skip -Dassembly.skipAssembly  -DnewVersion=1.7.0.0 -Dpython.ver="python >= 2.6"

