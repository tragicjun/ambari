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
// @todo: remove App.supports.kerberosAutomated after Kerberos Automation Wizard support

module.exports = App.WizardRoute.extend({
  route: '/service/add',

  enter: function (router) {
    console.log('in /service/add:enter');
    if (App.isAccessible('ADMIN')) {
      Em.run.next(function () {
        var addServiceController = router.get('addServiceController');
        App.router.get('updateController').set('isWorking', false);
        var popup = App.ModalPopup.show({
          classNames: ['full-width-modal'],
          header:Em.I18n.t('services.add.header'),
          bodyClass:  App.AddServiceView.extend({
            controllerBinding: 'App.router.addServiceController'
          }),
          primary:Em.I18n.t('form.cancel'),
          showFooter: false,
          secondary: null,

          onPrimary:function () {
            this.hide();
            App.router.transitionTo('main.services.index');
          },
          onClose: function() {
            this.set('showCloseButton', false); // prevent user to click "Close" many times
            App.router.get('updateController').set('isWorking', true);
            var self = this;
            App.router.get('updateController').updateServices(function(){
              App.router.get('updateController').updateServiceMetric();
            });
            var exitPath = addServiceController.getDBProperty('onClosePath') || 'main.services.index';
            addServiceController.finish();
            // We need to do recovery based on whether we are in Add Host or Installer wizard
            App.clusterStatus.setClusterStatus({
              clusterName: App.router.get('content.cluster.name'),
              clusterState: 'DEFAULT'
            }, {alwaysCallback: function() {self.hide();App.router.transitionTo(exitPath);location.reload();}});

          },
          didInsertElement: function(){
            this.fitHeight();
          }
        });
        addServiceController.set('popup',popup);
        var currentClusterStatus = App.clusterStatus.get('value');
        if (currentClusterStatus) {
          switch (currentClusterStatus.clusterState) {
            case 'ADD_SERVICES_DEPLOY_PREP_2' :
              addServiceController.setCurrentStep('5');
              break;
            case 'ADD_SERVICES_INSTALLING_3' :
            case 'SERVICE_STARTING_3' :
              addServiceController.setCurrentStep('6');
              break;
            case 'ADD_SERVICES_INSTALLED_4' :
              addServiceController.setCurrentStep('7');
              break;
            default:
              break;
          }
        }

        router.transitionTo('step' + addServiceController.get('currentStep'));
      });
    } else {
      Em.run.next(function () {
        App.router.transitionTo('main.services');
      });
    }

  },

  /*connectOutlets: function (router) {
    console.log('in /service/add:connectOutlets');
    router.get('mainController').connectOutlet('addService');
  },*/

  step1: Em.Route.extend({
    route: '/step1',
    connectOutlets: function (router) {
      console.log('in addService.step1:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep('1');
      controller.set('hideBackButton', true);
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          var wizardStep4Controller = router.get('wizardStep4Controller');
          wizardStep4Controller.set('wizardController', controller);
            //服务分类排序
            var items = controller.get('content.services').filterProperty('isInstallable', true);
            var category = App.service_category;
            var new_items = [];
            var arr_service = [];
            for (var key in category) {
                var flag = false;
                var services = category[key].join(',');
                for (var i=0; i<items.length; i++) {
                    var service_name = Em.get(items[i], 'serviceName').toUpperCase();
                    if (services.indexOf(service_name) != -1) {
                        if (!flag) {
                            Em.set(items[i], 'menuTitle', key);
                            flag = true;
                        }
                        arr_service.push(service_name);
                        new_items.push(items[i]);
                    }
                }
            }
            if (new_items.length != items.length) {
                var flag = false;
                var str_service = arr_service.join(',');
                for (var i=0; i<items.length; i++) {
                    var service_name = Em.get(items[i], 'serviceName').toUpperCase();
                    if (str_service.indexOf(service_name) == -1) {
                        if (!flag) {
                            Em.set(items[i], 'menuTitle', '其他');
                            flag = true;
                        }
                        new_items.push(items[i]);
                    }
                }
            }
          controller.connectOutlet('wizardStep4', new_items);
        });
      });
    },
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      var wizardStep4Controller = router.get('wizardStep4Controller');
      addServiceController.saveServices(wizardStep4Controller);
      addServiceController.saveClients(wizardStep4Controller);
      addServiceController.setDBProperty('masterComponentHosts', undefined);

      var wizardStep5Controller = router.get('wizardStep5Controller');
      wizardStep5Controller.clearRecommendations(); // Force reload recommendation between steps 1 and 2
      router.transitionTo('step2');
    }
  }),

  step2: Em.Route.extend({
    route: '/step2',
    connectOutlets: function (router) {
      console.log('in addService.step2:connectOutlets');
      var controller = router.get('addServiceController');
      var wizardStep2Controller = router.get('wizardStep5Controller');
      controller.setCurrentStep('2');
      controller.set('hideBackButton', false);
      wizardStep2Controller.set('isInitialLayout', true);
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          controller.connectOutlet('wizardStep5', controller.get('content'));
        });
      });

    },
    back: Em.Router.transitionTo('step1'),
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      var wizardStep5Controller = router.get('wizardStep5Controller');
      var wizardStep6Controller = router.get('wizardStep6Controller');
      addServiceController.saveMasterComponentHosts(wizardStep5Controller);
      addServiceController.setDBProperty('slaveComponentHosts', undefined);
      wizardStep6Controller.set('isClientsSet', false);
      router.transitionTo('step3');
    }
  }),

  step3: Em.Route.extend({
    route: '/step3',
    connectOutlets: function (router) {
      console.log('in addService.step3:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep('3');
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          var wizardStep6Controller = router.get('wizardStep6Controller');
          wizardStep6Controller.set('wizardController', controller);
          controller.connectOutlet('wizardStep6', controller.get('content'));
        });
      });
    },
    back: function(router){
      var controller = router.get('addServiceController');
      if(!controller.get('content.skipMasterStep')){
        router.transitionTo('step2');
      } else {
        router.transitionTo('step1');
      }
    },
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      var wizardStep6Controller = router.get('wizardStep6Controller');

      wizardStep6Controller.callValidation(function() {
        wizardStep6Controller.showValidationIssuesAcceptBox(function() {
          addServiceController.saveSlaveComponentHosts(wizardStep6Controller);
          addServiceController.get('content').set('serviceConfigProperties', null);
          addServiceController.setDBProperty('serviceConfigProperties', null);
          addServiceController.setDBProperty('groupsToDelete', []);
          router.transitionTo('step4');
        });
      });
    }
  }),

  step4: Em.Route.extend({
    route: '/step4',
    connectOutlets: function (router) {
      console.log('in addService.step4:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep('4');
      controller.dataLoading().done(function () {
        var wizardStep7Controller = router.get('wizardStep7Controller');
        controller.loadAllPriorSteps().done(function () {
          controller.loadAdvancedConfigs(wizardStep7Controller);
          wizardStep7Controller.getConfigTags();
          wizardStep7Controller.set('wizardController', controller);
          controller.usersLoading().done(function () {
            controller.connectOutlet('wizardStep7', controller.get('content'));
          });
        });
      });
    },
    back: function(router){
      var controller = router.get('addServiceController');
      if(!controller.get('content.skipSlavesStep')){
        router.transitionTo('step3');
      } else if(!controller.get('content.skipMasterStep')) {
        router.transitionTo('step2');
      } else {
        router.transitionTo('step1');
      }
    },
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      var wizardStep7Controller = router.get('wizardStep7Controller');
      addServiceController.saveServiceConfigProperties(wizardStep7Controller);
      addServiceController.saveServiceConfigGroups(wizardStep7Controller, true);
      if (App.supports.automatedKerberos) {
        if (router.get('mainAdminKerberosController.securityEnabled')) {
          router.transitionTo('step5');
          return;
        }
      }
      router.transitionTo('step6');
    }
  }),

  step5: Em.Route.extend({
    route: '/step5',
    connectOutlets: function (router) {
      var controller = router.get('addServiceController');
      controller.setCurrentStep('5');
      controller.dataLoading().done(function () {
        var kerberosStep4Controller = router.get('kerberosWizardStep4Controller');
        controller.loadAllPriorSteps().done(function () {
          kerberosStep4Controller.set('wizardController', controller);
          controller.connectOutlet('kerberosWizardStep4', controller.get('content'));
        });
      });
    },
    back: function(router){
      var controller = router.get('addServiceController');
      if(!controller.get('content.skipConfigStep')) {
        router.transitionTo('step4');
      }
      else {
        if(!controller.get('content.skipSlavesStep')) {
          router.transitionTo('step3');
        }
        else {
          if(!controller.get('content.skipMasterStep')) {
            router.transitionTo('step2');
          }
          else {
            router.transitionTo('step1');
          }
        }
      }
    },
    next: function (router) {
      if (App.supports.automatedKerberos && router.get('mainAdminKerberosController.securityEnabled')) {
        router.get('kerberosWizardStep2Controller').createKerberosAdminSession(router.get('kerberosWizardStep4Controller.stepConfigs')[0].get('configs'));
      }
      router.transitionTo('step6');
    }
  }),

  step6: Em.Route.extend({
    route: App.supports.automatedKerberos ? '/step6' : '/step5',
    connectOutlets: function (router, context) {
      console.log('in addService.step5:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep(App.supports.automatedKerberos ? '6' : '5');
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          var wizardStep8Controller = router.get('wizardStep8Controller');
          wizardStep8Controller.set('wizardController', controller);
          controller.connectOutlet('wizardStep8', controller.get('content'));
        });
      });
    },
    back: function(router){
      var controller = router.get('addServiceController');
      if (App.supports.automatedKerberos && router.get('mainAdminKerberosController.securityEnabled')) {
        router.transitionTo('step5');
        return;
      }
      if(!controller.get('content.skipConfigStep')) {
        router.transitionTo('step4');
      }
      else {
        if(!controller.get('content.skipSlavesStep')) {
          router.transitionTo('step3');
        }
        else {
          if(!controller.get('content.skipMasterStep')) {
            router.transitionTo('step2');
          }
          else {
            router.transitionTo('step1');
          }
        }
      }
    },
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      addServiceController.installServices(function () {
        router.get('wizardStep8Controller').set('servicesInstalled', true);
        addServiceController.setInfoForStep9();
        addServiceController.saveClusterState('ADD_SERVICES_INSTALLING_3');
        App.router.transitionTo('step7');
      });
    }
  }),

  step7: Em.Route.extend({
    route: App.supports.automatedKerberos ? '/step7' : '/step6',
    connectOutlets: function (router, context) {
      console.log('in addService.step6:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep(App.supports.automatedKerberos ? '7' : '6');
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          var wizardStep9Controller = router.get('wizardStep9Controller');
          wizardStep9Controller.set('wizardController', controller);
          if (!App.get('testMode')) {              //if test mode is ON don't disable prior steps link.
            controller.setLowerStepsDisable(App.supports.automatedKerberos ? 7 : 6);
          }
          controller.connectOutlet('wizardStep9', controller.get('content'));
        });
      });
    },
    back: Em.Router.transitionTo('step6'),
    retry: function(router,context) {
      var addServiceController = router.get('addServiceController');
      var wizardStep9Controller = router.get('wizardStep9Controller');
      if (wizardStep9Controller.get('showRetry')) {
        if (wizardStep9Controller.get('content.cluster.status') === 'INSTALL FAILED') {
          addServiceController.installServices(function () {
            addServiceController.setInfoForStep9();
            wizardStep9Controller.resetHostsForRetry();
            // We need to do recovery based on whether we are in Add Host or Installer wizard
            addServiceController.saveClusterState('ADD_SERVICES_INSTALLING_3');
            wizardStep9Controller.navigateStep();
          });
        } else {
          wizardStep9Controller.navigateStep();
        }
      }
    },
    unroutePath: function() {
      return false;
    },
    next: function (router) {
      var addServiceController = router.get('addServiceController');
      var wizardStep9Controller = router.get('wizardStep9Controller');
      addServiceController.saveInstalledHosts(wizardStep9Controller);

      // We need to do recovery based on whether we are in Add Host or Installer wizard
      addServiceController.saveClusterState('ADD_SERVICES_INSTALLED_4');
      router.transitionTo('step8');
    }
  }),

  step8: Em.Route.extend({
    route: App.supports.automatedKerberos ? '/step8' : '/step7',
    connectOutlets: function (router, context) {
      console.log('in addService.step7:connectOutlets');
      var controller = router.get('addServiceController');
      controller.setCurrentStep(App.supports.automatedKerberos ? '8' : '7');
      controller.dataLoading().done(function () {
        controller.loadAllPriorSteps().done(function () {
          controller.setLowerStepsDisable(App.supports.automatedKerberos ? 8 : 7);
          controller.connectOutlet('wizardStep10', controller.get('content'));
        });
      });
    },
    back: Em.Router.transitionTo('step7'),
    complete: function (router, context) {
      var addServiceController = router.get('addServiceController');
      addServiceController.get('popup').onClose();
    }
  }),

  backToServices: function (router) {
    App.router.get('updateController').set('isWorking', true);
    router.transitionTo('services');
  }

});
