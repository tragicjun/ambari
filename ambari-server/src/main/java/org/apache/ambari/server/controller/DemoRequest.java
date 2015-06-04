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

package org.apache.ambari.server.controller;

public class DemoRequest {

  private final Long demoId;

  private final String demoName;

  private final String demoValue;

  public DemoRequest(Long demoId, String demoName, String demoValue) {
    super();
    this.demoId = demoId;
    this.demoName = demoName;
    this.demoValue = demoValue;
  }

  /**
   * @return the demoId
   */
  public Long getDemoId() {
    return demoId;
  }

  /**
   * @return the demoName
   */
  public String getDemoName() {
    return demoName;
  }

  /**
   * @return the demoValue
   */
  public String getDemoValue() {
    return demoValue;
  }

  @Override
  public String toString() {
    return "DemoRequest{" +
             "demoId=" + demoId +
             ", demoName='" + demoName + '\'' +
             ", demoValue='" + demoValue + '\'' +
             '}';
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    DemoRequest that = (DemoRequest) o;

    if (demoId != null ? !demoId.equals(that.demoId) : that.demoId != null) return false;
    if (demoName != null ? !demoName.equals(that.demoName) : that.demoName != null) return false;
    if (demoValue != null ? !demoValue.equals(that.demoValue) : that.demoValue != null) return false;

    return true;
  }

  @Override
  public int hashCode() {
    int result = demoId != null ? demoId.hashCode() : 0;
    result = 31 * result + (demoName != null ? demoName.hashCode() : 0);
    result = 31 * result + (demoValue != null ? demoValue.hashCode() : 0);
    return result;
  }
}
