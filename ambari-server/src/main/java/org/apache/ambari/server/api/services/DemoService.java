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
import org.apache.ambari.server.controller.spi.Resource;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.HttpHeaders;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriInfo;
import java.util.Collections;


/**
 * Service responsible for test resource requests.
 */
@Path("/demos/")
public class DemoService extends BaseService {

  /**
   * The string utilities.
   */
  private final String msg;


  // ----- Constructors ------------------------------------------------------

  /**
   * Construct a TestService.
   */
  public DemoService() {
//    this.clusters = AmbariServer.getController().getClusters();
    msg = "demo service";
  }

  // ----- TestService ----------------------------------------------------

  /**
   * Handles: GET /demos/{demoID}
   * Get a specific demo.
   *
   * @param headers      http headers
   * @param ui           uri info
   * @param demoName     demo id
   *
   * @return demo instance representation
   */
  @GET
  @Path("{demoName}")
  @Produces("text/plain")
  public Response getDemo(String body, @Context HttpHeaders headers, @Context UriInfo ui,
                             @PathParam("demoName") String demoName) {

    return handleRequest(headers, body, ui, Request.Type.GET, createDemoResource(demoName));
  }
  /**
   * Handles: GET  /demos
   * Get all demos.
   *
   * @param headers  http headers
   * @param ui       uri info
   *
   * @return demo collection resource representation
   */
  @GET
  @Produces("text/plain")
  public Response getDemos(String body, @Context HttpHeaders headers, @Context UriInfo ui) {

    return handleRequest(headers, body, ui, Request.Type.GET, createDemoResource(null));
  }

  // ----- helper methods ----------------------------------------------------

  /**
   * Create a demo resource instance.
   *
   * @param demoName demo name
   *
   * @return a demo resource instance
   */
  ResourceInstance createDemoResource(String demoName) {
    return createResource(Resource.Type.Demo,
                           Collections.singletonMap(Resource.Type.Demo, demoName));
  }

}
