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

/**
 * Show prompt popup
 *
 * @param {String} text - additional text constant. Will be placed on the top of the input field
 * @param {Function} primary - "OK" button click handler
 * @param {String} defaultValue - additional text constant. Will be default value for input field
 * @param {Function} secondary
 * @return {*}
 */
App.showPromptPopup = function (text, primary, defaultValue, secondary) {
  if (!primary) {
    return false;
  }
  return App.ModalPopup.show({
    header: Em.I18n.t('popup.prompt.commonHeader'),
    bodyClass: Em.View.extend({
      templateName: require('templates/common/modal_popups/prompt_popup'),
      text: text
    }),
    inputValue: defaultValue || '',
    isInvalid: false,
    errorMessage: '',
    onPrimary: function () {
      this.hide();
      primary(this.get('inputValue'));
    },
    onSecondary: function () {
      this.hide();
      if (secondary) {
        secondary();
      }
    }
  });
};
