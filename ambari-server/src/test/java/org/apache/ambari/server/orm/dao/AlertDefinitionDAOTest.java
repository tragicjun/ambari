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

package org.apache.ambari.server.orm.dao;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.TimeZone;
import java.util.UUID;

import org.apache.ambari.server.orm.GuiceJpaInitializer;
import org.apache.ambari.server.orm.InMemoryDefaultTestModule;
import org.apache.ambari.server.orm.OrmTestHelper;
import org.apache.ambari.server.orm.entities.AlertCurrentEntity;
import org.apache.ambari.server.orm.entities.AlertDefinitionEntity;
import org.apache.ambari.server.orm.entities.AlertGroupEntity;
import org.apache.ambari.server.orm.entities.AlertHistoryEntity;
import org.apache.ambari.server.orm.entities.AlertNoticeEntity;
import org.apache.ambari.server.state.AlertState;
import org.apache.ambari.server.state.MaintenanceState;
import org.apache.ambari.server.state.NotificationState;
import org.apache.ambari.server.state.alert.Scope;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.google.inject.Guice;
import com.google.inject.Injector;
import com.google.inject.persist.PersistService;

/**
 * Tests {@link AlertDefinitionDAO} for interacting with
 * {@link AlertDefinitionEntity}.
 */
public class AlertDefinitionDAOTest {

  static Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("UTC"));

  Injector injector;
  Long clusterId;
  AlertDefinitionDAO dao;
  AlertsDAO alertsDao;
  AlertDispatchDAO dispatchDao;
  OrmTestHelper helper;

  /**
   *
   */
  @Before
  public void setup() {
    injector = Guice.createInjector(new InMemoryDefaultTestModule());
    injector.getInstance(GuiceJpaInitializer.class);

    dao = injector.getInstance(AlertDefinitionDAO.class);
    alertsDao = injector.getInstance(AlertsDAO.class);
    dispatchDao = injector.getInstance(AlertDispatchDAO.class);
    helper = injector.getInstance(OrmTestHelper.class);
    clusterId = helper.createCluster();

    for (int i = 0; i < 8; i++) {
      AlertDefinitionEntity definition = new AlertDefinitionEntity();
      definition.setDefinitionName("Alert Definition " + i);
      definition.setServiceName("HDFS");
      definition.setComponentName(null);
      definition.setClusterId(clusterId);
      definition.setHash(UUID.randomUUID().toString());
      definition.setScheduleInterval(60);
      definition.setScope(Scope.SERVICE);
      definition.setSource("Source " + i);
      definition.setSourceType("SCRIPT");
      dao.create(definition);
    }
  }

  @After
  public void teardown() {
    injector.getInstance(PersistService.class).stop();
    injector = null;
  }

  /**
   *
   */
  @Test
  public void testFindByName() {
    List<AlertDefinitionEntity> definitions = dao.findAll();
    Assert.assertNotNull(definitions);
    AlertDefinitionEntity definition = definitions.get(2);
    AlertDefinitionEntity retrieved = dao.findByName(
        definition.getClusterId(), definition.getDefinitionName());

    Assert.assertEquals(definition, retrieved);
  }

  /**
   *
   */
  @Test
  public void testFindAll() {
    List<AlertDefinitionEntity> definitions = dao.findAll();
    Assert.assertNotNull(definitions);
    Assert.assertEquals(8, definitions.size());
  }

  /**
   *
   */
  @Test
  public void findById() {
    List<AlertDefinitionEntity> definitions = dao.findAll();
    Assert.assertNotNull(definitions);
    AlertDefinitionEntity definition = definitions.get(2);
    AlertDefinitionEntity retrieved = dao.findById(definition.getDefinitionId());

    Assert.assertEquals(definition, retrieved);
  }

  @Test
  public void testRefresh() {
  }

  @Test
  public void testCreate() {
  }

  @Test
  public void testMerge() {
  }

  @Test
  public void testRemove() throws Exception {
    AlertDefinitionEntity definition = helper.createAlertDefinition(clusterId);
    definition = dao.findById(definition.getDefinitionId());
    assertNotNull(definition);
    dao.remove(definition);
    definition = dao.findById(definition.getDefinitionId());
    assertNull(definition);
  }

  /**
   * @throws Exception
   */
  @Test
  public void testCascadeDelete() throws Exception {
    AlertDefinitionEntity definition = helper.createAlertDefinition(clusterId);

    AlertGroupEntity group = helper.createAlertGroup(clusterId, null);
    group.getAlertDefinitions().add(definition);
    dispatchDao.merge(group);

    AlertHistoryEntity history = new AlertHistoryEntity();
    history.setServiceName(definition.getServiceName());
    history.setClusterId(clusterId);
    history.setAlertDefinition(definition);
    history.setAlertLabel("Label");
    history.setAlertState(AlertState.OK);
    history.setAlertText("Alert Text");
    history.setAlertTimestamp(calendar.getTimeInMillis());
    alertsDao.create(history);

    AlertCurrentEntity current = new AlertCurrentEntity();
    current.setAlertHistory(history);
    current.setLatestTimestamp(new Date().getTime());
    current.setOriginalTimestamp(new Date().getTime() - 10800000);
    current.setMaintenanceState(MaintenanceState.OFF);
    alertsDao.create(current);

    AlertNoticeEntity notice = new AlertNoticeEntity();
    notice.setAlertHistory(history);
    notice.setAlertTarget(helper.createAlertTarget());
    notice.setNotifyState(NotificationState.PENDING);
    notice.setUuid(UUID.randomUUID().toString());
    dispatchDao.create(notice);

    group = dispatchDao.findGroupById(group.getGroupId());
    assertNotNull(group);
    assertNotNull(group.getAlertDefinitions());
    assertEquals(1, group.getAlertDefinitions().size());

    history = alertsDao.findById(history.getAlertId());
    assertNotNull(history);

    current = alertsDao.findCurrentById(current.getAlertId());
    assertNotNull(current);
    assertNotNull(current.getAlertHistory());

    notice = dispatchDao.findNoticeById(notice.getNotificationId());
    assertNotNull(notice);
    assertNotNull(notice.getAlertHistory());
    assertNotNull(notice.getAlertTarget());

    // delete the definition
    definition = dao.findById(definition.getDefinitionId());
    dao.refresh(definition);
    dao.remove(definition);

    notice = dispatchDao.findNoticeById(notice.getNotificationId());
    assertNull(notice);

    current = alertsDao.findCurrentById(current.getAlertId());
    assertNull(current);

    history = alertsDao.findById(history.getAlertId());
    assertNull(history);

    group = dispatchDao.findGroupById(group.getGroupId());
    assertNotNull(group);
    assertNotNull(group.getAlertDefinitions());
    assertEquals(0, group.getAlertDefinitions().size());
  }
}
