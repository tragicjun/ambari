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

package org.apache.ambari.server.state.stack;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * Created by jerryjzhang on 15-6-4.
 */
public class StackServicePort {
    private Map<String,Map<String, List<String>>> content;

    public StackServicePort(){
    }

    public StackServicePort(Map<String,Map<String, List<String>>> content){
        this.content = content;
    }

    public Map<String, List<String>> getServicePort(String serviceName){
        return content.get(serviceName);
    }

    public List<String> getComponentPort(String serviceName, String componentName){
        List<String> ports = null;
        if(content != null) {
            Map<String, List<String>> servicePort = content.get(serviceName);
            if (servicePort != null) {
                ports = servicePort.get(componentName);
            }
        }
        return ports == null ? new ArrayList<String>() : ports;
    }

    public Map<String,Map<String, List<String>>> getContent(){
        return content;
    }

    public void merge(StackServicePort parent){
        //Map<String,Map<String, List<String>>> parentMap = parent.getContent();
    }
}
