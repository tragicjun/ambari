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
package org.apache.ambari.server.controller.internal;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.controller.AmbariManagementController;
import org.apache.ambari.server.controller.DemoRequest;
import org.apache.ambari.server.controller.DemoResponse;
import org.apache.ambari.server.controller.spi.NoSuchParentResourceException;
import org.apache.ambari.server.controller.spi.NoSuchResourceException;
import org.apache.ambari.server.controller.spi.Predicate;
import org.apache.ambari.server.controller.spi.Request;
import org.apache.ambari.server.controller.spi.RequestStatus;
import org.apache.ambari.server.controller.spi.Resource;
import org.apache.ambari.server.controller.spi.ResourceAlreadyExistsException;
import org.apache.ambari.server.controller.spi.SystemException;
import org.apache.ambari.server.controller.spi.UnsupportedPropertyException;
import org.apache.ambari.server.controller.utilities.PropertyHelper;

/**
 * Resource provider for cluster resources.
 */
public class DemoResourceProvider extends BaseBlueprintProcessor {

  // ----- Property ID constants ---------------------------------------------

  // Demos
  protected static final String DEMO_ID_PROPERTY_ID      = PropertyHelper.getPropertyId("Demos", "demo_id");
  protected static final String DEMO_NAME_PROPERTY_ID    = PropertyHelper.getPropertyId("Demos", "demo_name");
  protected static final String DEMO_VALUE_PROPERTY_ID   = PropertyHelper.getPropertyId("Demos", "demo_value");

  // ----- Constructors ----------------------------------------------------

  /**
   * Create a  new resource provider for the given management controller.
   *
   * @param propertyIds           the property ids
   * @param keyPropertyIds        the key property ids
   * @param managementController  the management controller
   */
  DemoResourceProvider(Set<String> propertyIds,
                       Map<Resource.Type, String> keyPropertyIds,
                       AmbariManagementController managementController) {

    super(propertyIds, keyPropertyIds, managementController);
  }


  // ----- ResourceProvider ------------------------------------------------

  /**
   * Create the resources defined by the properties in the given request object.
   *
   * @param request the request object which defines the set of properties
   *                for the resources to be created
   * @return the request status
   * @throws org.apache.ambari.server.controller.spi.SystemException                an internal system exception occurred
   * @throws org.apache.ambari.server.controller.spi.UnsupportedPropertyException   the request contains unsupported property ids
   * @throws org.apache.ambari.server.controller.spi.ResourceAlreadyExistsException attempted to create a resource which already exists
   * @throws org.apache.ambari.server.controller.spi.NoSuchParentResourceException  a parent resource of the resource to create doesn't exist
   */
  @Override
  public RequestStatus createResources(Request request) throws SystemException, UnsupportedPropertyException, ResourceAlreadyExistsException, NoSuchParentResourceException {
    return null;
  }

  @Override
  public Set<Resource> getResources(Request request, Predicate predicate)
      throws SystemException, UnsupportedPropertyException, NoSuchResourceException, NoSuchParentResourceException {

    final Set<DemoRequest> requests = new HashSet<DemoRequest>();

    Set<String> requestedIds = getRequestPropertyIds(request, predicate);

    Set<DemoResponse> responses = getResources(new Command<Set<DemoResponse>>() {
      @Override
      public Set<DemoResponse> invoke() throws AmbariException {
        return getManagementController().getDemos(requests);
      }
    });

    Set<Resource> resources = new HashSet<Resource>();
    if (LOG.isDebugEnabled()) {
      LOG.debug("Found demos matching getDemos request"
          + ", demoResponseCount=" + responses.size());
    }

    for (DemoResponse response : responses) {

      String demoName = response.getDemoName();
      String demoValue = response.getDemoValue();

      Resource resource = new ResourceImpl(Resource.Type.Demo);
      setResourceProperty(resource, DEMO_ID_PROPERTY_ID, response.getDemoId(), requestedIds);
      setResourceProperty(resource, DEMO_NAME_PROPERTY_ID, demoName, requestedIds);
      setResourceProperty(resource, DEMO_VALUE_PROPERTY_ID, demoValue, requestedIds);

      if (LOG.isDebugEnabled()) {
        LOG.debug("Adding DemoResponse to resource"
            + ", demoResponse=" + response.toString());
      }
      resources.add(resource);
    }
    return resources;
  }

  /**
   * Update the resources selected by the given predicate with the properties
   * from the given request object.
   *
   * @param request   the request object which defines the set of properties
   *                  for the resources to be updated
   * @param predicate the predicate object which can be used to filter which
   *                  resources are updated
   * @return the request status
   * @throws org.apache.ambari.server.controller.spi.SystemException               an internal system exception occurred
   * @throws org.apache.ambari.server.controller.spi.UnsupportedPropertyException  the request contains unsupported property ids
   * @throws org.apache.ambari.server.controller.spi.NoSuchResourceException       the resource instance to be updated doesn't exist
   * @throws org.apache.ambari.server.controller.spi.NoSuchParentResourceException a parent resource of the resource doesn't exist
   */
  @Override
  public RequestStatus updateResources(Request request, Predicate predicate) throws SystemException, UnsupportedPropertyException, NoSuchResourceException, NoSuchParentResourceException {
    return null;
  }

  /**
   * Delete the resources selected by the given predicate.
   *
   * @param predicate the predicate object which can be used to filter which
   *                  resources are deleted
   * @return the request status
   * @throws org.apache.ambari.server.controller.spi.SystemException               an internal system exception occurred
   * @throws org.apache.ambari.server.controller.spi.UnsupportedPropertyException  the request contains unsupported property ids
   * @throws org.apache.ambari.server.controller.spi.NoSuchResourceException       the resource instance to be deleted doesn't exist
   * @throws org.apache.ambari.server.controller.spi.NoSuchParentResourceException a parent resource of the resource doesn't exist
   */
  @Override
  public RequestStatus deleteResources(Predicate predicate) throws SystemException, UnsupportedPropertyException, NoSuchResourceException, NoSuchParentResourceException {
    return null;
  }
  
  /**
   * The cluster primary key properties.
   */
  private static Set<String> pkPropertyIds =
      new HashSet<String>(Arrays.asList(new String[]{DEMO_ID_PROPERTY_ID}));

  /**
   * Get the set of property ids that uniquely identify the resources
   * of this provider.
   *
   * @return the set of primary key properties
   */
  @Override
  protected Set<String> getPKPropertyIds() {
    return pkPropertyIds;
  }
}

