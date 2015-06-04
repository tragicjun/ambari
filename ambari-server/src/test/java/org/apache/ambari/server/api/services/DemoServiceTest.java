/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.ambari.server.api.services;

import org.apache.ambari.server.api.resources.ResourceInstance;
import org.apache.ambari.server.api.services.parsers.RequestBodyParser;
import org.apache.ambari.server.api.services.serializers.ResultSerializer;
import org.apache.ambari.server.state.Clusters;
import org.apache.ambari.server.state.cluster.ClustersImpl;

import javax.ws.rs.core.HttpHeaders;
import javax.ws.rs.core.UriInfo;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertEquals;


/**
 * Unit tests for ClusterService.
 */
public class DemoServiceTest extends BaseServiceTest {

  private class TestDemoService extends DemoService {

    @Override
    ResourceInstance createDemoResource(String demoName) {
      return getTestResource();
    }

    @Override
    RequestFactory getRequestFactory() {
      return getTestRequestFactory();
    }

    @Override
    protected RequestBodyParser getBodyParser() {
      return getTestBodyParser();
    }

    @Override
    protected ResultSerializer getResultSerializer() {
      return getTestResultSerializer();
    }
  }

  public List<ServiceTestInvocation> getTestInvocations() throws Exception {
    List<ServiceTestInvocation> listInvocations = new ArrayList<ServiceTestInvocation>();

    //getCluster
    DemoService demoService = new TestDemoService();
    Method m;
    Object[] args;
//    m = demoService.getClass().getMethod("getDemo", String.class, HttpHeaders.class, UriInfo.class, String.class);
//    args = new Object[] {null, getHttpHeaders(), getUriInfo(), "demoName"};
//    listInvocations.add(new ServiceTestInvocation(Request.Type.GET, demoService, m, args, null));

    //getClusters
    m = demoService.getClass().getMethod("getDemos", String.class, HttpHeaders.class, UriInfo.class);
    args = new Object[] {null, getHttpHeaders(), getUriInfo()};
    listInvocations.add(new ServiceTestInvocation(Request.Type.GET, demoService, m, args, null));

    return listInvocations;
  }

  //todo: test getHostHandler, getServiceHandler, getHostComponentHandler
}
