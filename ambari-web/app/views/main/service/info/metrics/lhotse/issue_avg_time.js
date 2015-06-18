/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with this
 * work for additional information regarding copyright ownership. The ASF
 * licenses this file to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

var App = require('app');

/**
 * @class
 * 
 * This is a view for showing lhotse issue average time metrics
 * 
 * @extends App.ChartLinearTimeView
 * @extends Ember.Object
 * @extends Ember.View
 */
App.ChartServiceMetricsLhotse_IssueAvgTime= App.ChartLinearTimeView.extend({
  id: "service-metrics-lhotse-issue-avg-time",
  title: Em.I18n.t('services.service.info.metrics.lhotse.issueAvgTime'),
  yAxisFormatter: App.ChartLinearTimeView.TimeElapsedFormatter,
  renderer: 'line',
  ajaxIndex: 'service.metrics.lhotse.issue_avg_time',

  transformToSeries: function (jsonData) {
    var seriesArray = [];
    if (jsonData && jsonData.metrics && jsonData.metrics.lhotse_file && jsonData.metrics.lhotse_file.metrics_file && jsonData.metrics.lhotse_file.metrics_file.issue_avg_time) {
      for ( var name in jsonData.metrics.lhotse_file.metrics_file.issue_avg_time) {
        var seriesData = jsonData.metrics.lhotse_file.metrics_file.issue_avg_time[name];
        var displayName = App.lhotse_task_type[name];
        if (seriesData) {
          var s = this.transformData(seriesData, displayName);
          seriesArray.push(s);
        }
      }
    }
    return seriesArray;
  }
});

