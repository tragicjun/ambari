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


App.widgetMapper = App.QuickDataMapper.create({
  model: App.Widget,
  config: {
    id: 'id',
    widget_name: 'widget_name',
    default_order: 'default_order',
    widget_type: 'widget_type',
    display_name: 'display_name',
    service_name: 'service_name',
    component_name: 'component_name',
    section_name: 'section_name',
    time_created: 'time_created',
    author: 'author',
    properties: 'properties',
    metrics: 'metrics',
    values: 'values',
    description: 'description',
    is_visible: 'is_visible'
  },
  map: function (json, serviceName) {
    //TODO add service name to user layout API response
    if (!this.get('model')) return;

    if (json) {
      var result = [];

      var sectionName = json.section_name;
      json.widgetLayoutInfo.forEach(function (item, index) {
        item.service_name = serviceName;
        item.section_name = sectionName;
        item.id = item.widget_name + "_" + (item.id || "0");     // user created widgets will have id as their primary id. stack created widgets will not have id and will have their widget_name as unique id
        item.default_order = (index + 1);
        result.push(this.parseIt(item, this.config));
      }, this);

      App.store.loadMany(this.get('model'), result);
    }
  }
});
