/*
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

package org.apache.ambari.server.audit;

import org.apache.ambari.server.api.services.Request;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import javax.ws.rs.core.Response;

/**
 * Declare rest api audit
 */
public abstract class Auditor {

  /**
   * Set a mark
   */
  public abstract void mark();

  /**
   * Record audit message
   * @param message
   */
  public abstract void record(String message);

  /**
   * Record api request and response
   * @param request
   * @param response
   */
  public abstract void record(Request request, Response response);

  /**
   * Get current user
   *
   * @return login user name
   */
  protected String currentUser() {
    SecurityContext securityContext = SecurityContextHolder.getContext();
    String currentUserName = securityContext.getAuthentication().getName();
    return currentUserName;
  }
}
