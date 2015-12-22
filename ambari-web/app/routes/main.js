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
var stringUtils = require('utils/string_utils');

module.exports = Em.Route.extend(App.RouterRedirections, {
  route: '/main',
  enter: function (router) {
    App.db.updateStorage();
    console.log('in /main:enter');
    var self = this;
    router.getAuthenticated().done(function (loggedIn) {
      if (loggedIn) {
        var applicationController = App.router.get('applicationController');
        applicationController.startKeepAlivePoller();
        App.router.get('mainController').checkServerClientVersion().done(function () {
          App.router.get('mainViewsController').loadAmbariViews();
          App.router.get('clusterController').loadClusterName(false).done(function () {
            if (App.get('testMode')) {
              router.get('mainController').initialize();
            } else {
              if (router.get('clusterInstallCompleted')) {
                App.router.get('clusterController').loadClientServerClockDistance().done(function () {
                  App.router.get('clusterController').checkDetailedRepoVersion().done(function () {
                    router.get('mainController').initialize();
                  });
                });
              }
              else {
                Em.run.next(function () {
                  App.clusterStatus.updateFromServer().complete(function () {
                    var currentClusterStatus = App.clusterStatus.get('value');
                    if (router.get('currentState.parentState.name') !== 'views'
                        && currentClusterStatus && self.get('installerStatuses').contains(currentClusterStatus.clusterState)) {
                      if (App.isAccessible('ADMIN')) {
                        self.redirectToInstaller(router, currentClusterStatus, false);
                      } else {
                        Em.run.next(function () {
                          App.router.transitionTo('main.views.index');
                        });
                      }
                    }
                  });
                });
                App.router.get('clusterController').set('isLoaded', true);
              }
            }
          });
        });
        // TODO: redirect to last known state
      } else {
        router.set('preferedPath', router.location.location.hash);
        Em.run.next(function () {
          router.transitionTo('login');
        });
      }
    });
  },
  /*
   routePath: function(router,event) {
   if (router.getAuthenticated()) {
   App.router.get('clusterController').loadClusterName(false);
   router.get('mainController').initialize();
   // TODO: redirect to last known state
   } else {
   Ember.run.next(function () {
   router.transitionTo('login');
   });
   }
   }, */

  index: Ember.Route.extend({
    route: '/',
    redirectsTo: 'dashboard.index'
  }),

  connectOutlets: function (router, context) {
    router.get('applicationController').connectOutlet('main');
  },

  test: Em.Route.extend({
    route: '/test',
    connectOutlets: function (router, context) {
      router.get('mainController').connectOutlet('mainTest');
    }
  }),

  dashboard: Em.Route.extend({
    route: '/dashboard',
    connectOutlets: function (router, context) {
      router.get('mainController').connectOutlet('mainDashboard');
    },
    index: Em.Route.extend({
      route: '/',
      enter: function (router) {
        Em.run.next(function () {
          router.transitionTo('main.dashboard.widgets');
        });
      }
    }),
    goToDashboardView: function (router, event) {
      router.transitionTo(event.context);
    },
    widgets: Em.Route.extend({
      route: '/metrics',
      connectOutlets: function (router, context) {
        router.set('mainDashboardController.selectedCategory', 'widgets');
        router.get('mainDashboardController').connectOutlet('mainDashboardWidgets');
      }
    }),
    charts: Em.Route.extend({
      route: '/charts',
      connectOutlets: function (router, context) {
        router.set('mainDashboardController.selectedCategory', 'charts');
        router.get('mainDashboardController').connectOutlet('mainCharts');
      },
      index: Ember.Route.extend({
        route: '/',
        enter: function (router) {
          Em.run.next(function () {
            router.transitionTo('heatmap');
          });
        }
      }),
      heatmap: Em.Route.extend({
        route: '/heatmap',
        connectOutlets: function (router, context) {
          router.get('mainChartsController').connectOutlet('mainChartsHeatmap');
        }
      }),
      horizon_chart: Em.Route.extend({
        route: '/horizon_chart',
        connectOutlets: function (router, context) {
          router.get('mainChartsController').connectOutlet('mainChartsHorizon');
        }
      }),
      showChart: function (router, event) {
        var parent = event.view._parentView;
        parent.deactivateChildViews();
        event.view.set('active', "active");
        router.transitionTo(event.context);
      }
    }),
    configHistory: Em.Route.extend({
      route: '/config_history',
      connectOutlets: function (router, context) {
        router.set('mainDashboardController.selectedCategory', 'configHistory');
        router.get('mainDashboardController').connectOutlet('mainConfigHistory');
      }
    }),
    goToServiceConfigs: function (router, event) {
      router.get('mainServiceItemController').set('routeToConfigs', true);
      router.get('mainServiceInfoConfigsController').set('preSelectedConfigVersion', event.context);
      router.transitionTo('main.services.service.configs', App.Service.find(event.context.get('serviceName')));
      router.get('mainServiceItemController').set('routeToConfigs', false);
    }
  }),

  views: require('routes/views'),

  hosts: Em.Route.extend({
    route: '/hosts',
    index: Ember.Route.extend({
      route: '/',
      connectOutlets: function (router, context) {
        router.get('mainController').connectOutlet('mainHost');
      }
    }),

    hostDetails: Em.Route.extend({
      route: '/:host_id',
      connectOutlets: function (router, host) {
        router.get('mainHostController').set('showFilterConditionsFirstLoad', true);
        router.get('mainController').connectOutlet('mainHostDetails', host);
      },

      index: Ember.Route.extend({
        route: '/',
        redirectsTo: 'summary'
      }),

      summary: Em.Route.extend({
        route: '/summary',
        connectOutlets: function (router, context) {
          router.get('mainController').dataLoading().done(function() {
            var controller = router.get('mainHostDetailsController');
            if ( App.Service.find().mapProperty('serviceName').contains('OOZIE')) {
              controller.loadConfigs('loadOozieConfigs');
              controller.isOozieConfigLoaded.always(function () {
                controller.connectOutlet('mainHostSummary');
              });
            }else {
              controller.connectOutlet('mainHostSummary');
            }
          });
        }
      }),

      configs: Em.Route.extend({
        route: '/configs',
        connectOutlets: function (router, context) {
          router.get('mainHostDetailsController').connectOutlet('mainHostConfigs');
        }
      }),

      alerts: Em.Route.extend({
        route: '/alerts',
        connectOutlets: function (router, context) {
          router.get('mainHostDetailsController').connectOutlet('mainHostAlerts');
        },
        exit: function (router) {
          router.set('mainAlertInstancesController.isUpdating', false);
        }
      }),

      metrics: Em.Route.extend({
        route: '/metrics',
        connectOutlets: function (router, context) {
          router.get('mainHostDetailsController').connectOutlet('mainHostMetrics');
        }
      }),

      stackVersions: Em.Route.extend({
        route: '/stackVersions',
        connectOutlets: function (router, context) {
          if (App.get('stackVersionsAvailable')) {
            router.get('mainHostDetailsController').connectOutlet('mainHostStackVersions');
          }
          else {
            router.transitionTo('summary');
          }
        }
      }),

      hostNavigate: function (router, event) {
        var parent = event.view._parentView;
        parent.deactivateChildViews();
        event.view.set('active', "active");
        router.transitionTo(event.context);
      }
    }),

    back: function (router, event) {
      var referer = router.get('mainHostDetailsController.referer');
      if (referer) {
        router.route(referer);
      }
      else {
        window.history.back();
      }
    },

    addHost: function (router) {
      router.transitionTo('hostAdd');
    }

  }),

  hostAdd: require('routes/add_host_routes'),

  alerts: Em.Route.extend({
    route: '/alerts',
    index: Em.Route.extend({
      route: '/',
      connectOutlets: function (router, context) {
        router.get('mainController').connectOutlet('mainAlertDefinitions');
      }
    }),

    alertDetails: Em.Route.extend({

      route: '/:alert_definition_id',

      connectOutlets: function (router, alertDefinition) {
        App.router.set('mainAlertDefinitionsController.showFilterConditionsFirstLoad', true);
        router.get('mainController').connectOutlet('mainAlertDefinitionDetails', alertDefinition);
      },

      exit: function (router) {
        router.set('mainAlertInstancesController.isUpdating', false);
      },

      unroutePath: function (router, context) {
        var controller = router.get('mainAlertDefinitionDetailsController');
        if (!controller.get('forceTransition') && controller.get('isEditing')) {
          controller.showSavePopup(context);
        } else {
          controller.set('forceTransition', false);
          this._super(router, context);
        }
      }
    }),

    back: function (router, event) {
      window.history.back();
    }
  }),

  alertAdd: require('routes/add_alert_definition_routes'),

  admin: Em.Route.extend({
    route: '/admin',
    enter: function (router, transition) {
      if (router.get('loggedIn') && !App.isAccessible('upgrade_ADMIN')) {
        Em.run.next(function () {
          router.transitionTo('main.dashboard.index');
        });
      }
    },

    routePath: function (router, event) {
      if (!App.isAccessible('upgrade_ADMIN')) {
        Em.run.next(function () {
          App.router.transitionTo('main.dashboard.index');
        });
      } else {
        this._super(router, event);
      }
    },
    connectOutlets: function (router, context) {
      router.get('mainController').connectOutlet('mainAdmin');
    },

    index: Em.Route.extend({
      /* enter: function(router, transition){
       var controller = router.get('mainAdminController');
       router.transitionTo('admin' + controller.get('category').capitalize());
       }, */
      route: '/',
      redirectsTo: 'stackAndUpgrade.index'
    }),

    adminAuthentication: Em.Route.extend({
      route: '/authentication',
      connectOutlets: function (router, context) {
        router.set('mainAdminController.category', "authentication");
        router.get('mainAdminController').connectOutlet('mainAdminAuthentication');
      }
    }),

    adminSecurity: Em.Route.extend({
      route: '/security',
      enter: function (router) {
        router.set('mainAdminController.category', "security");
        var controller = router.get('mainAdminSecurityController');
        if (!(controller.getAddSecurityWizardStatus() === 'RUNNING') && !(controller.getDisableSecurityStatus() === 'RUNNING')) {
          Em.run.next(function () {
            router.transitionTo('adminSecurity.index');
          });
        } else if (controller.getAddSecurityWizardStatus() === 'RUNNING') {
          Em.run.next(function () {
            router.transitionTo('adminAddSecurity');
          });
        } else if (controller.getDisableSecurityStatus() === 'RUNNING') {
          Em.run.next(function () {
            router.transitionTo('disableSecurity');
          });
        }
      },

      index: Em.Route.extend({
        route: '/',
        connectOutlets: function (router, context) {
          var controller = router.get('mainAdminController');
          controller.set('category', "security");
          controller.connectOutlet('mainAdminSecurity');
        }
      }),

      addSecurity: function (router, object) {
        router.get('mainAdminSecurityController').setAddSecurityWizardStatus('RUNNING');
        router.transitionTo('adminAddSecurity');
      },

      adminAddSecurity: require('routes/add_security')
    }),

    adminKerberos: Em.Route.extend({
      route: '/kerberos',
      index: Em.Route.extend({
        route: '/',
        connectOutlets: function (router, context) {
          router.set('mainAdminController.category', "kerberos");
          router.get('mainAdminController').connectOutlet('mainAdminKerberos');
        }
      }),
      adminAddKerberos: require('routes/add_kerberos_routes'),

      disableSecurity: Em.Route.extend({
        route: '/disableSecurity',
        enter: function (router) {
          App.router.get('updateController').set('isWorking', false);
          router.get('mainController').dataLoading().done(function() {
            App.ModalPopup.show({
              classNames: ['full-width-modal'],
              header: Em.I18n.t('admin.removeSecurity.header'),
              bodyClass: App.KerberosDisableView.extend({
                controllerBinding: 'App.router.kerberosDisableController'
              }),
              primary: Em.I18n.t('form.cancel'),
              secondary: null,
              showFooter: false,

              onClose: function () {
                var self = this;
                var controller = router.get('kerberosDisableController');
                if (!controller.get('isSubmitDisabled')) {
                  self.proceedOnClose();
                  return;
                }
                // warn user if disable kerberos command in progress
                var unkerberizeCommand = controller.get('tasks').findProperty('command', 'unkerberize');
                if (unkerberizeCommand && !unkerberizeCommand.get('isCompleted')) {
                  // user cannot exit wizard during removing kerberos
                  if (unkerberizeCommand.get('status') == 'IN_PROGRESS') {
                    App.showAlertPopup(Em.I18n.t('admin.kerberos.disable.unkerberize.header'), Em.I18n.t('admin.kerberos.disable.unkerberize.message'));
                  } else {
                    // otherwise show confirmation window
                    App.showConfirmationPopup(function () {
                      self.proceedOnClose();
                    }, Em.I18n.t('admin.addSecurity.disable.onClose'));
                  }
                } else {
                  self.proceedOnClose();
                }
              },
              proceedOnClose: function () {
                var self = this;
                var disableController = router.get('kerberosDisableController');
                disableController.clearStep();
                disableController.resetDbNamespace();
                App.db.setSecurityDeployCommands(undefined);
                App.router.get('updateController').set('isWorking', true);
                router.get('mainAdminKerberosController').setDisableSecurityStatus(undefined);
                router.get('addServiceController').finish();
                App.clusterStatus.setClusterStatus({
                  clusterName: router.get('content.cluster.name'),
                  clusterState: 'DEFAULT',
                  localdb: App.db.data
                }, {
                  alwaysCallback: function() {
                    self.hide();
                    router.transitionTo('adminKerberos.index');
                    location.reload();
                  }
                });
              },
              didInsertElement: function () {
                this.fitHeight();
              }
            });
          });
        },

        unroutePath: function () {
          return false;
        },
        next: function (router, context) {
          $("#modal").find(".close").trigger('click');
        },
        done: function (router, context) {
          var controller = router.get('kerberosDisableController');
          if (!controller.get('isSubmitDisabled')) {
            $(context.currentTarget).parents("#modal").find(".close").trigger('click');
          }
        }
      })
    }),

    stackAndUpgrade: Em.Route.extend({
      route: '/stack',
      connectOutlets: function (router) {
        router.set('mainAdminController.category', "stackAndUpgrade");
        router.get('mainAdminController').connectOutlet('mainAdminStackAndUpgrade');
      },

      index: Em.Route.extend({
        route: '/',
        redirectsTo: 'services'
      }),

      services: Em.Route.extend({
        route: '/services',
        connectOutlets: function (router, context) {
          router.get('mainAdminStackAndUpgradeController').connectOutlet('mainAdminStackServices');
        }
      }),

      versions: Em.Route.extend({
        route: '/versions',
        connectOutlets: function (router, context) {
          router.get('mainAdminStackAndUpgradeController').connectOutlet('MainAdminStackVersions');
        }
      }),

      stackNavigate: function (router, event) {
        var parent = event.view._parentView;
        parent.deactivateChildViews();
        event.view.set('active', "active");
        router.transitionTo(event.context);
      }
    }),
    stackUpgrade: require('routes/stack_upgrade_routes'),

    adminAdvanced: Em.Route.extend({
      route: '/advanced',
      connectOutlets: function (router) {
        router.set('mainAdminController.category', "advanced");
        router.get('mainAdminController').connectOutlet('mainAdminAdvanced');
      }
    }),
    adminServiceAccounts: Em.Route.extend({
      route: '/serviceAccounts',
      connectOutlets: function (router) {
        router.set('mainAdminController.category', "adminServiceAccounts");
        router.get('mainAdminController').connectOutlet('mainAdminServiceAccounts');
      }
    }),

    adminAudit: Em.Route.extend({
      route: '/audit',
      connectOutlets: function (router) {
        router.set('mainAdminController.category', "audit");
        router.get('mainAdminController').connectOutlet('mainAdminAudit');
      }
    }),
    upgradeStack: function (router, event) {
      if (!$(event.currentTarget).hasClass('inactive')) {
        router.transitionTo('stackUpgrade');
      }
    },


    adminNavigate: function (router, object) {
      router.transitionTo('admin' + object.context.capitalize());
    },

    //events
    goToAdmin: function (router, event) {
      router.transitionTo(event.context);
    }

  }),

  services: Em.Route.extend({
    route: '/services',
    index: Em.Route.extend({
      route: '/',
      enter: function (router) {
        Em.run.next(function () {
          var controller = router.get('mainController');
          controller.dataLoading().done(function () {
            if (router.currentState.parentState.name === 'services' && router.currentState.name === 'index') {
              var service = router.get('mainServiceItemController.content');
              if (!service || !service.get('isLoaded')) {
                service = App.Service.find().objectAt(0); // getting the first service to display
              }
              if (router.get('mainServiceItemController').get('routeToConfigs')) {
                router.transitionTo('service.configs', service);
              } else {
                router.transitionTo('service.summary', service);
              }
            }
          });
        });
      }
    }),
    connectOutlets: function (router, context) {
      router.get('mainController').connectOutlet('mainService');
    },
    service: Em.Route.extend({
      route: '/:service_id',
      connectOutlets: function (router, service) {
        router.get('mainServiceController').connectOutlet('mainServiceItem', service);
        if (service && router.get('mainServiceItemController').get('routeToConfigs')) {
          router.transitionTo('configs');
        } else {
          router.transitionTo('summary');
        }
      },
      index: Ember.Route.extend({
        route: '/'
      }),
      summary: Em.Route.extend({
        route: '/summary',
        connectOutlets: function (router, context) {
          var item = router.get('mainServiceItemController.content');
          //if service is not existed then route to default service
          if (item.get('isLoaded')) {
            router.get('mainServiceItemController').connectOutlet('mainServiceInfoSummary', item);
          } else {
            router.transitionTo('services.index');
          }
        }
      }),
      metrics: Em.Route.extend({
        route: '/metrics',
        connectOutlets: function (router, context) {
          var item = router.get('mainServiceItemController.content');
          router.get('mainServiceItemController').connectOutlet('mainServiceInfoMetrics', item);
        }
      }),
      configs: Em.Route.extend({
        route: '/configs',
        connectOutlets: function (router, context) {
          var item = router.get('mainServiceItemController.content');
          //if service is not existed then route to default service
          if (item.get('isLoaded')) {
            if (router.get('mainServiceItemController.isConfigurable')) {
              router.get('mainServiceItemController').connectOutlet('mainServiceInfoConfigs', item);
            }
            else {
              // if service doesn't have configs redirect to summary
              router.transitionTo('summary');
            }
          }
          else {
            item.set('routeToConfigs', true);
            router.transitionTo('services.index');
          }
        },
        unroutePath: function (router, context) {
          var controller = router.get('mainServiceInfoConfigsController');
          if (!controller.get('forceTransition') && controller.hasUnsavedChanges()) {
            controller.showSavePopup(context);
          } else {
            this._super(router, context);
          }
        }
      }),
      audit: Em.Route.extend({
        route: '/audit',
        connectOutlets: function (router, context) {
          var item = router.get('mainServiceItemController.content');
          router.get('mainServiceItemController').connectOutlet('mainServiceInfoAudit', item);
        }
      }),
        showHost : function () {

            var numberUtils = require('utils/number_utils');
            if ($('#hostListDiv').length > 0) {
                $('#hostListDiv').show();
            } else {
                $('.nav-tabs').next().next().after('<div id="hostListDiv">loading...</div>');
            }
            $('.nav-tabs').next().next().hide();
            var prefix = App.get('apiPrefix') + '/clusters/' + App.router.getClusterName();

            var url = prefix + '/hosts?fields=Hosts/host_name,Hosts/maintenance_state,Hosts/public_host_name,Hosts/cpu_count,Hosts/ph_cpu_count,alerts_summary,'
                + 'Hosts/host_status,Hosts/last_heartbeat_time,Hosts/ip,host_components/HostRoles/state,host_components/HostRoles/maintenance_state,'
                + 'host_components/HostRoles/stale_configs,host_components/HostRoles/service_name,host_components/HostRoles/desired_admin_state,'
                + 'metrics/disk,metrics/load/load_one,Hosts/total_mem,stack_versions/HostStackVersions,stack_versions/repository_versions/RepositoryVersions/repository_version,'
                + 'stack_versions/repository_versions/RepositoryVersions/id,stack_versions/repository_versions/RepositoryVersions/display_name&minimal_response=true&sortBy=Hosts/host_name.asc';

            var hash = window.location.hash;

            var service_name = hash.split('/')[3];
            $.getJSON(url, function(json){
                var list = json.items;
                var data = {};
                var length = 0;
                for (var i=0; i<list.length; i++) {
                    var flag = 0;
                    var d = list[i]['host_components'];
                    for (var j=0; j<d.length; j++) {
                        if (d[j]['HostRoles']['service_name'] == service_name) {
                            flag = 1;
                            if (typeof (data[d[j]['HostRoles']['component_name']]) == 'undefined') {
                                data[d[j]['HostRoles']['component_name']] = [list[i]];
                            } else {
                                data[d[j]['HostRoles']['component_name']].push(list[i]);
                            }
                        }
                    }
                    if (flag == 1) {
                        length ++;
                    }
                }
                var str = '<div id="hostList" class="host-list">';
                str += '<div class="hd"><button  class="btn btn-success" id="btn_restart">重启</button><h3 class="modules"><i class="icon-ok-sign health-status-LIVE"></i>'+service_name+'</h3><h3 class="hosts">'+length+'主机</h3></div><div class="bd open">';
                str +='<table class="host-table">';
                str += '<tr><th class="modules">包含组件</th><th class="host">运行的主机</th><th class="trigger"></th></tr>';
                var flag = 0;
                for (var key in data) {
                    str += flag==0 ? '<tr class="open">' : '<tr>';
                    str += '<td class="modules">'+'<input type="checkbox" class="sum_select_all" style="vertical-align: middle;display: inline-block;margin: -2px 10px 0;"/><span class="host_name">'+key+'</span></td><td class="host">'+data[key].length+'主机</td><td class="trigger"><i class="caret"></i></td><div></div></tr>';
                    str += flag==0 ? '<tr class="open show-detail">' : '<tr class="show-detail">';
                    //str += '<tr class="show-detail">';
                    flag = 1;

                    str += '<td colspan="3"><table class="detail-table">';
                    str += '<tr><th>名字</th><th>IP地址</th><th>Cores (CPU)</th><th>内存</th><th>磁盘用量</th><th>平均负载</th></tr>';
                    for (var i=0; i<data[key].length; i++) {
                        str += '<tr>';
                        // host_status
                        str += '<td><div class="host-name"><input type="checkbox" class="input_restart" style="vertical-align: middle;display: inline-block;margin: -2px 10px 0;"/><i class="icon-ok-sign health-status-LIVE"></i><a href="#/main/hosts/'+data[key][i].Hosts.ip+'/summary">'+data[key][i].Hosts.host_name+'</a></div></td>';
                        str += '<td><div class="host-ip">'+data[key][i].Hosts.ip+'</div></td>';
                        str += '<td>'+data[key][i].Hosts.cpu_count+'('+data[key][i].Hosts.ph_cpu_count+')</td>';
                        str += '<td>'+numberUtils.bytesToSize(data[key][i].Hosts.total_mem, 2, 'parseFloat', 1024)+'</td>';

                        if (typeof(data[key][i].metrics) == 'undefined') {
                            str += '<td></td><td></td>';
                        } else {
                            var process = Math.round(((data[key][i].metrics.disk.disk_total-data[key][i].metrics.disk.disk_free)/data[key][i].metrics.disk.disk_total) * Math.pow(10, 4)) / Math.pow(10, 2);

                            str += '<td><div class="progress-wrap"><div class="progress progress-info"><div style="width:'+process+'%" class="bar"></div></div><span>'+process+'%</span></div></td>';
                            // metrics/load/load_one
                            str += '<td>'+Math.round(data[key][i].metrics.load.load_one * Math.pow(10, 2)) / Math.pow(10, 4)+'</td>';
                        }
                        str += '</tr>';
                        // loadAvg
                    }
                    str += '</table></td>';

                    str += '</tr>';
                }
                str += '</table>';
                str += '</div>';
                $('#hostListDiv').html(str);
                //$('#hostListDiv').find('.caret').parent().parent().click(function(){
                    $('#hostListDiv').find('.caret').click(function(){
                        var $this = $(this).parent().parent();
                        var target = $this.next();
                        if (!target.hasClass('open')) {
                            $this.addClass('open');
                            target.addClass('open');
                        } else {
                            target.removeClass('open');
                            $this.removeClass('open');
                        }
                    });
                    $('.sum_select_all').bind('click', function(){
                        var $this = $(this);
                        if($this.is(':checked') === true) {
                            $this.parent().parent().next().find('.input_restart').attr("checked", true);
                        } else {
                            $this.parent().parent().next().find('.input_restart').attr("checked", false);
                        }
                    });
                    $('#btn_restart').bind('click', function(){
                        var host = "";
                        var restartComponents = [];
                        $('.input_restart:checked').each(function(){
                            var name = $(this).parent().parent().parent().parent().parent().parent().parent().prev().find('span[class="host_name"]').text();
                            host += name + ' ：'  + $(this).next().next().text() + "<br/>";
                            var host_name = $(this).parent().parent().parent().parent().parent().parent().parent().prev().find('.host_name').text();
                            restartComponents.push({
                                restartComponents : host_name,
                                hostName : $(this).parent().parent().next().find('.host-ip').text(),
                                serviceName : $('#btn_restart').next().text()
                            });

                        });
                        if(host === '') {
                            App.showAlertPopup(Em.I18n.t('common.error'), '请选择待重启的组件');
                            return false;
                        }
                        var defaultSuccessCallback = function(data, ajaxOptions, params) {
                            App.router.get('applicationController').dataLoading().done(function(initValue) {
                                params.query && params.query.set('status', 'SUCCESS');
                                if (initValue) {
                                    App.router.get('backgroundOperationsController').showPopup();
                                }
                            });
                        };
                        var defaultErrorCallback = function(xhr, textStatus, error, opt, params) {
                            params.query && params.query.set('status', 'FAIL');
                            App.ajax.defaultErrorHandler(xhr, opt.url, 'POST', xhr.status);
                        };
                        var batches =[];
                        if(restartComponents.length > 0) {
                            for(count=0; count<restartComponents.length; count++) {
                                batches.push({
                                    "order_id" : count + 1,
                                    "type" : "POST",
                                    "uri" : App.apiPrefix + "/clusters/" + App.get('clusterName') + "/requests",
                                    "RequestBodyInfo" : {
                                        "RequestInfo" : {
                                            "context" : "_PARSE_.ROLLING-RESTART." + restartComponents[count].restartComponents + "." + (count + 1) + "." + restartComponents.length,
                                            "command" : "RESTART"
                                        },
                                        "Requests/resource_filters": [{
                                            "service_name" : restartComponents[count].serviceName,
                                            "component_name" : restartComponents[count].restartComponents,
                                            "hosts" : restartComponents[count].hostName
                                        }]
                                    }
                                });
                            }
                        }
                        var div_str = '<table><tbody>' +
                            '<tr><td><span>重启</span></td><td><input class="ember-view ember-text-field span1" type="text" value="1"></td><td>个Runner每次</td></tr>' +
                            '<tr><td><span>等候 </span></td><td><input id="service_intervalTimeSeconds" class="ember-view ember-text-field span1" type="text" value="120"></td><td><span>秒每批次之间</span></td></tr>' +
                            '<tr><td><span>容忍</span></td><td><input id="service_tolerateSize" class="ember-view ember-text-field span1" type="text" value="1"></td><td><span>次重启失败</span></td></tr>' +
                            '</tbody></table>';

                        App.ModalPopup.show({
                            header : "灰度重启以下主机：",
                            bodyClass : Em.View.extend({
                                template : Em.Handlebars.compile('<div class="alert alert-warning">' + host + '</div>' + div_str)
                            }),
                            classNames : [ 'rolling-restart-popup' ],
                            primary : Em.I18n.t('rollingrestart.dialog.primary'),
                            onPrimary : function() {
                                var dialog = this;
                                var intervalTimeSeconds = $.trim($("#service_intervalTimeSeconds").val());
                                if(intervalTimeSeconds === "") {
                                    intervalTimeSeconds = 120;
                                } else {
                                    intervalTimeSeconds = parseInt(intervalTimeSeconds);
                                }
                                var tolerateSize = $.trim($("#service_tolerateSize").val());
                                if(tolerateSize === "") {
                                    tolerateSize = 1;
                                } else {
                                    tolerateSize = parseInt(tolerateSize);
                                }
                                App.ajax.send({
                                    name: 'rolling_restart.post',
                                    sender: {
                                        successCallback: defaultSuccessCallback,
                                        errorCallback: defaultErrorCallback
                                    },
                                    data: {
                                        intervalTimeSeconds: intervalTimeSeconds,
                                        tolerateSize: tolerateSize,
                                        batches: batches
                                    },
                                    success: 'successCallback',
                                    error: 'errorCallback'
                                });
                                dialog.hide();
                            }
                        });
                    });
            });
        },
      showInfo: function (router, event) {
		var self = this;
        var mainServiceInfoConfigsController = App.router.get('mainServiceInfoConfigsController');
        if (event.context === 'summary' && mainServiceInfoConfigsController.hasUnsavedChanges()) {
          mainServiceInfoConfigsController.showSavePopup(router.get('location.lastSetURL').replace('configs', 'summary'));
          return false;
        }
        var parent = event.view.get('_parentView');
        parent.deactivateChildViews();
        event.view.set('active', "active");
		if (event.context == 'hostTab') {
			self.showHost();
			return;
		} else {
			$('.nav-tabs').next().next().show();
			$('#hostListDiv').hide();
		}
        router.transitionTo(event.context);
      }
    }),
    showService: Em.Router.transitionTo('service'),
    addService: Em.Router.transitionTo('serviceAdd'),
    reassign: Em.Router.transitionTo('reassign'),

    enableHighAvailability: require('routes/high_availability_routes'),

    enableRMHighAvailability: require('routes/rm_high_availability_routes'),

    rollbackHighAvailability: require('routes/rollbackHA_routes')
  }),

  reassign: require('routes/reassign_master_routes'),

  serviceAdd: require('routes/add_service_routes'),

  selectService: Em.Route.transitionTo('services.service.summary'),
  selectHost: function (router, event) {
    router.get('mainHostDetailsController').set('isFromHosts', false);
    router.transitionTo('hosts.hostDetails.index', event.context);
  },
  filterHosts: function (router, component) {
    if (!component.context)
      return;
    router.get('mainHostController').filterByComponent(component.context);
    router.get('mainHostController').set('showFilterConditionsFirstLoad', true);
    router.transitionTo('hosts.index');
  },
  showDetails: function (router, event) {
    router.get('mainHostDetailsController').set('referer', router.location.lastSetURL);
    router.get('mainHostDetailsController').set('isFromHosts', true);
    router.transitionTo('hosts.hostDetails.summary', event.context);
  },
  gotoAlertDetails: function (router, event) {
    router.transitionTo('alerts.alertDetails', event.context);
  },

  /**
   * Open summary page of the selected service
   * @param {object} event
   * @method routeToService
   */
  routeToService: function (router, event) {
    var service = event.context;
    router.transitionTo('main.services.service.summary', service);
  }
});
