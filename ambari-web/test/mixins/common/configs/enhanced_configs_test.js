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

describe('App.EnhancedConfigsMixin', function() {

  var mixinObject = Em.Controller.extend(App.EnhancedConfigsMixin, {});
  var instanceObject = mixinObject.create({});
  describe('#removeCurrentFromDependentList()', function() {
    it('update some fields', function() {
      instanceObject.get('_dependentConfigValues').pushObject({
          saveRecommended: true,
          saveRecommendedDefault: true,
          propertyName: 'p1',
          fileName: 'f1',
          value: 'v1'
        });
      instanceObject.removeCurrentFromDependentList(Em.Object.create({name: 'p1', filename: 'f1.xml', value: 'v2'}));
      expect(instanceObject.get('_dependentConfigValues')[0]).to.eql({
        saveRecommended: false,
        saveRecommendedDefault: false,
        propertyName: 'p1',
        fileName: 'f1',
        value: 'v2'
      });
    });
  });
});

