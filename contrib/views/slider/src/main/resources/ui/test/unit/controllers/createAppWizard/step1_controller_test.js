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

moduleFor('controller:createAppWizardStep1', 'App.CreateAppWizardStep1Controller', {

  needs: [
    'controller:createAppWizard'
  ]

});

test('isAppTypesError', function () {

  var controller = this.subject({availableTypes: {content: []}});
  equal(controller.get('isAppTypesError'), true, 'should be true if no app types provided');

  Em.run(function () {
    controller.set('availableTypes', {content: [
      {}
    ]});
  });
  equal(controller.get('isAppTypesError'), false, 'should be false if app types provided');

});

test('nameValidator', function () {
  expect(7);

  var tests = [
    { name: 'Slider', e: true },
    { name: '_slider', e: true },
    { name: 'slider*2', e: true },
    { name: 'slider', e: false },
    { name: 'slider_1-2_3', e: false }
  ];

  var controller = this.subject({isNameError: false,
    store: Em.Object.create({
      all: function (key) {
        return {
          sliderApp: [
            { name: 'slider2' }
          ]
        }[key];
      }
    })
  });

  tests.forEach(function (test) {
    Em.run(function () {
      controller.set('newApp', { name: test.name});
    });

    equal(controller.get('isNameError'), test.e, 'Name `' + test.name + '` is' + (!!test.e ? ' not ' : ' ') + 'valid');
  });

  Em.run(function () {
    controller.set('newApp', { name: 'slider2'});
  });

  equal(controller.get('isNameError'), true, 'Name `slider2` already exist');
  equal(controller.get('nameErrorMessage'), Em.I18n.t('wizard.step1.nameRepeatError'), 'Error message should be shown');
});

test('validateAppNameSuccessCallback', function () {

  var selectedType = Em.Object.create({
      id: 'HBASE',
      configs: {
        n0: 'v0'
      }
    }),
    title = 'newApp should have {0} set',
    controller = this.subject({
      newApp: Em.Object.create(),
      selectedType: selectedType
    });

  Em.run(function () {
    controller.set('appWizardController.transitionToRoute', Em.K);
    controller.validateAppNameSuccessCallback();
  });

  deepEqual(controller.get('newApp.appType'), selectedType, title.format('appType'));
  deepEqual(controller.get('newApp.configs'), selectedType.configs, title.format('configs'));
  deepEqual(controller.get('newApp.predefinedConfigNames'), Em.keys(selectedType.configs), title.format('predefinedConfigNames'));
  deepEqual(controller.get('appWizardController.newApp'), controller.get('newApp'), 'newApp should be set in CreateAppWizardController');
  equal(controller.get('appWizardController.currentStep'), 2, 'should proceed to the next step');

});

test('isSubmitDisabled', function () {

  expect(6);

  var controller = this.subject({
      availableTypes: {
        content: [
          {}
        ]
      },
      isNameError: false,
      newApp: {
        name: 'some'
      }
    }),
    cases = [
      {
        key: 'validateAppNameRequestExecuting',
        title: 'request is executing'
      },
      {
        key: 'isNameError',
        title: 'app name is invalid'
      },
      {
        key: 'no app types are available',
        title: 'request is executing'
      },
      {
        key: 'isFrequencyError',
        title: 'frequency value is invalid'
      }
    ],
    keys = cases.mapProperty('key'),
    failTitle = 'submit button is disabled when {0}';

  equal(controller.get('isSubmitDisabled'), false);

  cases.forEach(function (item) {
    Em.run(function () {
      keys.forEach(function (key) {
        controller.set(key, item.key != key);
      });
    });
    equal(controller.get('isSubmitDisabled'), true, failTitle.format(item.title));
  });

  Em.run(function () {
    keys.forEach(function (key) {
      controller.set(key, true);
    });
    controller.set('newApp.name', '');
  });
  equal(controller.get('isSubmitDisabled'), true, failTitle.format('no app name is specified'));

});

test('frequencyValidator', function () {

  expect(8);

  var controller = this.subject(),
    cases = [
      {
        value: '123',
        isFrequencyError: false,
        frequencyErrorMessage: '',
        title: 'numeric value'
      },
      {
        value: '123a',
        isFrequencyError: true,
        frequencyErrorMessage: Em.I18n.t('wizard.step1.frequencyError'),
        title: 'value contains letter'
      },
      {
        value: '123-',
        isFrequencyError: true,
        frequencyErrorMessage: Em.I18n.t('wizard.step1.frequencyError'),
        title: 'value contains special symbol'
      },
      {
        value: '123 ',
        isFrequencyError: true,
        frequencyErrorMessage: Em.I18n.t('wizard.step1.frequencyError'),
        title: 'value contains space'
      }
    ],
    errorTitle = '{0}: isFrequencyError is set correctly',
    messageTitle = '{0}: error message is set correctly';

  cases.forEach(function (item) {
    Em.run(function () {
      controller.set('newApp', {
        frequency: item.value
      });
    });
    equal(controller.get('isFrequencyError'), item.isFrequencyError, errorTitle.format(item.title));
    equal(controller.get('frequencyErrorMessage'), item.frequencyErrorMessage, messageTitle.format(item.title));
  });

});