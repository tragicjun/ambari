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

App.GraphWidgetView = Em.View.extend(App.WidgetMixin, {
  templateName: require('templates/common/widget/graph_widget'),

  /**
   * common metrics container
   * @type {Array}
   */
  metrics: [],

  /**
   * value in ms
   * @type {number}
   */
  timeRange: 3600,

  /**
   * value in ms
   * @type {number}
   */
  timeStep: 15,

  /**
   * @type {Array}
   */
  data: [],

  drawWidget: function () {
    if (this.get('isLoaded')) {
      this.set('data', this.calculateValues());
    }
  },

  /**
   * calculate series datasets for graph widgets
   */
  calculateValues: function () {
    var metrics = this.get('metrics');
    var seriesData = [];

    this.get('content.values').forEach(function (value) {
      var expression =  this.extractExpressions(value)[0];
      var computedExpressions;

      if (expression) {
        computedExpressions = this.computeExpression(expression, metrics);
        seriesData.push({
          name: value.name,
          data: computedExpressions[value.value.match(this.get('EXPRESSION_REGEX'))[0]]
        });
      }
    }, this);
    return seriesData;
  },

  /**
   * compute expression
   *
   * @param {string} expression
   * @param {object} metrics
   * @returns {object}
   */
  computeExpression: function (expression, metrics) {
    var validExpression = true,
      value = [],
      dataLinks = {},
      dataLength = 0,
      beforeCompute,
      result = {};

    //replace values with metrics data
    expression.match(this.get('VALUE_NAME_REGEX')).forEach(function (match) {
      if (metrics.someProperty('name', match)) {
        dataLinks[match] = metrics.findProperty('name', match).data;
        dataLength = metrics.findProperty('name', match).data.length;
      } else {
        validExpression = false;
        console.warn('Metrics not found to compute expression');
      }
    });

    if (validExpression) {
      for (var i = 0, timestamp; i < dataLength; i++) {
        beforeCompute = expression.replace(this.get('VALUE_NAME_REGEX'), function (match) {
          timestamp = dataLinks[match][i][1];
          return dataLinks[match][i][0];
        });
        value.push([Number(window.eval(beforeCompute)), timestamp]);
      }
    }

    result['${' + expression + '}'] = value;
    return result;
  },

  /**
   * make GET call to server in order to fetch service-component metrics
   * @param {object} request
   * @returns {$.ajax}
   */
  getServiceComponentMetrics: function (request) {
    return App.ajax.send({
      name: 'widgets.serviceComponent.metrics.get',
      sender: this,
      data: {
        serviceName: request.service_name,
        componentName: request.component_name,
        widgetIds: this.addTimeProperties(request.widget_ids).join(',')
      },
      success: 'getServiceComponentMetricsSuccessCallback'
    });
  },

  /**
   * make GET call to server in order to fetch host-component metrics
   * @param {object} request
   * @returns {$.ajax}
   */
  getHostComponentMetrics: function (request) {
    return App.ajax.send({
      name: 'widgets.hostComponent.metrics.get',
      sender: this,
      data: {
        serviceName: request.service_name,
        componentName: request.component_name,
        widgetIds: this.addTimeProperties(request.widget_ids).join(','),
        hostComponentCriteria: 'host_components/HostRoles/' + request.host_component_criteria
      },
      success: 'getHostComponentMetricsSuccessCallback'
    });
  },

  /**
   * add time properties
   * @param {Array} widgetIds
   * @returns {Array} result
   */
  addTimeProperties: function (widgetIds) {
    var startDate = App.dateTime();
    var endDate = startDate + this.get('timeRange');
    var step = this.get('timeStep');
    var result = [];

    widgetIds.forEach(function (ambariId) {
      result.push(ambariId + '[' + startDate + ',' + endDate + ',' + step + ']');
    }, this);

    return result;
  },

  /**
   * @type {Em.View}
   * @class
   */
  graphView: App.ChartLinearTimeView.extend({

    /**
     * graph height
     * @type {number}
     */
    height: 95,

    /**
     * @type {string}
     */
    id: function () {
      return this.get('parentView.content.id') + '_graph';
    }.property('parentView.content.id'),

    /**
     * @type {string}
     */
    renderer: function () {
      return this.get('parentView.content.properties.graph_type') === 'STACK' ? 'area' : 'line';
    }.property('parentView.content.properties.graph_type'),

    transformToSeries: function (seriesData) {
      var seriesArray = [];

      seriesData.forEach(function(_series){
        seriesArray.push(this.transformData(_series.data, _series.name));
      }, this);
      return seriesArray;
    },

    didInsertElement: function () {
      this._refreshGraph(this.get('parentView.data'));
    }.observes('parentView.data')
  })
});