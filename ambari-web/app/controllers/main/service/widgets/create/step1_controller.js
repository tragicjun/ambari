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

var App = require('app');

App.WidgetWizardStep1Controller = Em.Controller.extend({
  name: "widgetWizardStep1Controller",

  /**
   * Types:
   * - GAUGE
   * - NUMBER
   * - GRAPH
   * - TEMPLATE
   * @type {string}
   */
  widgetType: '',

  /**
   * @type {boolean}
   */
  isSubmitDisabled: function() {
    return !this.get('widgetType');
  }.property('widgetType'),

  /**
   * @type {App.WidgetType}
   */
  options: App.WidgetType.find(),

  loadStep: function() {
    this.clearStep();
  },

  clearStep: function() {
    this.set('widgetType', '');
  },

  next: function () {
    if (!this.get('isSubmitDisabled')) {
      App.router.send('next');
    }
  }
});

