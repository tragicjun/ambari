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
package org.apache.ambari.server.actionmanager;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.agent.CommandReport;
import org.apache.ambari.server.agent.ExecutionCommand;
import org.apache.ambari.server.orm.dao.ClusterDAO;
import org.apache.ambari.server.orm.dao.ExecutionCommandDAO;
import org.apache.ambari.server.orm.dao.HostDAO;
import org.apache.ambari.server.orm.dao.HostRoleCommandDAO;
import org.apache.ambari.server.orm.dao.RequestDAO;
import org.apache.ambari.server.orm.dao.RequestScheduleDAO;
import org.apache.ambari.server.orm.dao.RoleSuccessCriteriaDAO;
import org.apache.ambari.server.orm.dao.StageDAO;
import org.apache.ambari.server.orm.entities.ClusterEntity;
import org.apache.ambari.server.orm.entities.ExecutionCommandEntity;
import org.apache.ambari.server.orm.entities.HostEntity;
import org.apache.ambari.server.orm.entities.HostRoleCommandEntity;
import org.apache.ambari.server.orm.entities.RequestEntity;
import org.apache.ambari.server.orm.entities.RequestScheduleEntity;
import org.apache.ambari.server.orm.entities.RoleSuccessCriteriaEntity;
import org.apache.ambari.server.orm.entities.StageEntity;
import org.apache.ambari.server.state.Clusters;
import org.apache.ambari.server.state.Host;
import org.apache.ambari.server.utils.StageUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import com.google.inject.Inject;
import com.google.inject.Singleton;
import com.google.inject.name.Named;
import com.google.inject.persist.Transactional;

@Singleton
public class ActionDBAccessorImpl implements ActionDBAccessor {
  private static final Logger LOG = LoggerFactory.getLogger(ActionDBAccessorImpl.class);

  private long requestId;

  @Inject
  ClusterDAO clusterDAO;

  @Inject
  HostDAO hostDAO;

  @Inject
  RequestDAO requestDAO;

  @Inject
  StageDAO stageDAO;

  @Inject
  HostRoleCommandDAO hostRoleCommandDAO;

  @Inject
  ExecutionCommandDAO executionCommandDAO;

  @Inject
  RoleSuccessCriteriaDAO roleSuccessCriteriaDAO;

  @Inject
  StageFactory stageFactory;

  @Inject
  RequestFactory requestFactory;

  @Inject
  HostRoleCommandFactory hostRoleCommandFactory;

  @Inject
  Clusters clusters;

  @Inject
  RequestScheduleDAO requestScheduleDAO;

  private Cache<Long, HostRoleCommand> hostRoleCommandCache;
  private long cacheLimit; //may be exceeded to store tasks from one request

  @Inject
  public ActionDBAccessorImpl(@Named("executionCommandCacheSize") long cacheLimit) {

    this.cacheLimit = cacheLimit;
    hostRoleCommandCache = CacheBuilder.newBuilder().
        expireAfterAccess(5, TimeUnit.MINUTES).
        build();

  }

  @Inject
  void init() {
    requestId = stageDAO.getLastRequestId();
  }

  /* (non-Javadoc)
   * @see org.apache.ambari.server.actionmanager.ActionDBAccessor#getStage(java.lang.String)
   */
  @Override
  public Stage getStage(String actionId) {
    StageEntity stageEntity = stageDAO.findByActionId(actionId);
    return stageFactory.createExisting(stageEntity);
  }

  /* (non-Javadoc)
   * @see org.apache.ambari.server.actionmanager.ActionDBAccessor#getAllStages(java.lang.String)
   */
  @Override
  public List<Stage> getAllStages(long requestId) {
    List<Stage> stages = new ArrayList<Stage>();
    for (StageEntity stageEntity : stageDAO.findByRequestId(requestId)) {
      stages.add(stageFactory.createExisting(stageEntity));
    }
    return stages;
  }

  @Override
  public Request getRequest(long requestId) {
    RequestEntity requestEntity = requestDAO.findByPK(requestId);
    if (requestEntity != null) {
      return requestFactory.createExisting(requestEntity);
    } else {
      return null;
    }
  }

  /* (non-Javadoc)
   * @see org.apache.ambari.server.actionmanager.ActionDBAccessor#abortOperation(long)
   */
  @Override
  public void abortOperation(long requestId) {
    long now = System.currentTimeMillis();

    endRequest(requestId);

    List<HostRoleCommandEntity> commands =
        hostRoleCommandDAO.findByRequest(requestId);
    for (HostRoleCommandEntity command : commands) {
      if (command.getStatus() == HostRoleStatus.QUEUED ||
          command.getStatus() == HostRoleStatus.IN_PROGRESS ||
          command.getStatus() == HostRoleStatus.PENDING) {

        command.setStatus(HostRoleStatus.ABORTED);
        command.setEndTime(now);
        LOG.info("Aborting command. Hostname " + command.getHostName()
            + " role " + command.getRole()
            + " requestId " + command.getRequestId()
            + " taskId " + command.getTaskId()
            + " stageId " + command.getStageId());
      }
    }

    hostRoleCommandDAO.mergeAll(commands);
  }

  /* (non-Javadoc)
   * @see org.apache.ambari.server.actionmanager.ActionDBAccessor#timeoutHostRole(long, long, org.apache.ambari.server.Role)
   */
  @Override
  public void timeoutHostRole(String host, long requestId, long stageId,
                              String role) {
    long now = System.currentTimeMillis();
    List<HostRoleCommandEntity> commands =
        hostRoleCommandDAO.findByHostRole(host, requestId, stageId, role);
    for (HostRoleCommandEntity command : commands) {
      command.setStatus(HostRoleStatus.TIMEDOUT);
      command.setEndTime(now);
    }
    hostRoleCommandDAO.mergeAll(commands);
    endRequestIfCompleted(requestId);
  }

  /**
   * {@inheritDoc}
   */
  @Override
  public List<Stage> getStagesInProgress() {
    List<Stage> stages = new ArrayList<Stage>();
    List<StageEntity> stageEntities = stageDAO.findByCommandStatuses(HostRoleStatus.IN_PROGRESS_STATUSES);

    for (StageEntity stageEntity : stageEntities) {
      stages.add(stageFactory.createExisting(stageEntity));
    }

    return stages;
  }

  /**
   * {@inheritDoc}
   */
  @Override
  public int getCommandsInProgressCount() {
    Number count = hostRoleCommandDAO.getCountByStatus(HostRoleStatus.IN_PROGRESS_STATUSES);
    if (null == count) {
      return 0;
    }

    return count.intValue();
  }

  @Override
  @Transactional
  public void persistActions(Request request) throws AmbariException {

    RequestEntity requestEntity = request.constructNewPersistenceEntity();

    Long clusterId = Long.valueOf(-1L);
    ClusterEntity clusterEntity = clusterDAO.findById(request.getClusterId());
    if (clusterEntity != null) {
      clusterId = clusterEntity.getClusterId();
    }

    requestEntity.setClusterId(clusterId);
    requestDAO.create(requestEntity);

    //TODO wire request to cluster
    List<StageEntity> stageEntities = new ArrayList<StageEntity>(request.getStages().size());

    for (Stage stage : request.getStages()) {
      StageEntity stageEntity = stage.constructNewPersistenceEntity();
      stageEntities.add(stageEntity);
      stageEntity.setClusterId(clusterId);
      //TODO refactor to reduce merges
      stageEntity.setRequest(requestEntity);
      stageDAO.create(stageEntity);

      List<HostRoleCommand> orderedHostRoleCommands = stage.getOrderedHostRoleCommands();
      List<HostRoleCommandEntity> hostRoleCommandEntities = new ArrayList<HostRoleCommandEntity>();

      for (HostRoleCommand hostRoleCommand : orderedHostRoleCommands) {
        HostRoleCommandEntity hostRoleCommandEntity = hostRoleCommand.constructNewPersistenceEntity();
        hostRoleCommandEntities.add(hostRoleCommandEntity);
        hostRoleCommandEntity.setStage(stageEntity);

        HostEntity hostEntity = hostDAO.findByName(hostRoleCommandEntity.getHostName());
        if (hostEntity == null) {
          String msg = String.format("Host %s doesn't exist in database", hostRoleCommandEntity.getHostName());
          LOG.error(msg);
          throw new AmbariException(msg);
        }
        hostRoleCommandEntity.setHost(hostEntity);
        hostRoleCommandDAO.create(hostRoleCommandEntity);

        assert hostRoleCommandEntity.getTaskId() != null;
        hostRoleCommand.setTaskId(hostRoleCommandEntity.getTaskId());

        try {
          // Get the in-memory host object and its prefix to construct the output and error log paths.
          Host hostObject = clusters.getHost(hostRoleCommandEntity.getHostName());
          String prefix = hostObject.getPrefix();
          if (null != prefix && !prefix.isEmpty()) {
            if (!prefix.endsWith("/")) {
              prefix = prefix + "/";
            }
            hostRoleCommand.setOutputLog(prefix + "output-" + hostRoleCommandEntity.getTaskId() + ".txt");
            hostRoleCommand.setErrorLog(prefix + "errors-" + hostRoleCommandEntity.getTaskId() + ".txt");
            hostRoleCommandEntity.setOutputLog(hostRoleCommand.getOutputLog());
            hostRoleCommandEntity.setErrorLog(hostRoleCommand.getErrorLog());
          }
        } catch (AmbariException e) {
          LOG.warn("Exception in getting prefix for host and setting output and error log files.");
        }

        ExecutionCommandEntity executionCommandEntity = hostRoleCommand.constructExecutionCommandEntity();
        executionCommandEntity.setHostRoleCommand(hostRoleCommandEntity);

        executionCommandEntity.setTaskId(hostRoleCommandEntity.getTaskId());
        hostRoleCommandEntity.setExecutionCommand(executionCommandEntity);

        executionCommandDAO.create(hostRoleCommandEntity.getExecutionCommand());
        hostRoleCommandDAO.merge(hostRoleCommandEntity);
        hostDAO.merge(hostEntity);
      }

      for (RoleSuccessCriteriaEntity roleSuccessCriteriaEntity : stageEntity.getRoleSuccessCriterias()) {
        roleSuccessCriteriaDAO.create(roleSuccessCriteriaEntity);
      }

      stageDAO.create(stageEntity);
    }
    requestEntity.setStages(stageEntities);
    requestDAO.merge(requestEntity);
  }

  @Override
  public void startRequest(long requestId) {
    RequestEntity requestEntity = requestDAO.findByPK(requestId);
    if (requestEntity != null && requestEntity.getStartTime() == -1L) {
      requestEntity.setStartTime(System.currentTimeMillis());
      requestDAO.merge(requestEntity);
    }
  }

  @Override
  public void endRequest(long requestId) {
    RequestEntity requestEntity = requestDAO.findByPK(requestId);
    if (requestEntity != null && requestEntity.getEndTime() == -1L) {
      requestEntity.setEndTime(System.currentTimeMillis());
      requestDAO.merge(requestEntity);
    }
  }

  public void endRequestIfCompleted(long requestId) {
    if (requestDAO.isAllTasksCompleted(requestId)) {
      endRequest(requestId);
    }
  }

  @Override
  @Transactional
  public void setSourceScheduleForRequest(long requestId, long scheduleId) {
    RequestEntity requestEntity = requestDAO.findByPK(requestId);
    if (requestEntity != null) {
      RequestScheduleEntity scheduleEntity = requestScheduleDAO.findById(scheduleId);
      if (scheduleEntity != null) {
        requestEntity.setRequestScheduleEntity(scheduleEntity);
        //we may want to break entity graph here for perf purposes (when list size is too large)
        scheduleEntity.getRequestEntities().add(requestEntity);

        requestDAO.merge(requestEntity);
        requestScheduleDAO.merge(scheduleEntity);

      } else {
        String message = String.format("Request Schedule with id=%s not found", scheduleId);
        LOG.error(message);
        throw new RuntimeException(message);
      }

    } else {
      String message = String.format("Request with id=%s not found", scheduleId);
      LOG.error(message);
      throw new RuntimeException(message);
    }
  }

  @Override
  public void updateHostRoleStates(Collection<CommandReport> reports) {
    Map<Long, CommandReport> taskReports = new HashMap<Long, CommandReport>();
    for (CommandReport report : reports) {
      taskReports.put(report.getTaskId(), report);
    }

    long now = System.currentTimeMillis();

    List<Long> requestsToCheck = new ArrayList<Long>();
    List<Long> abortedCommandUpdates = new ArrayList<Long>();

    List<HostRoleCommandEntity> commandEntities = hostRoleCommandDAO.findByPKs(taskReports.keySet());
    for (HostRoleCommandEntity commandEntity : commandEntities) {
      CommandReport report = taskReports.get(commandEntity.getTaskId());
      if (commandEntity.getStatus() != HostRoleStatus.ABORTED) {
        // We don't want to overwrite statuses for ABORTED tasks with
        // statuses that have been received from the agent after aborting task
        commandEntity.setStatus(HostRoleStatus.valueOf(report.getStatus()));
      } else {
        abortedCommandUpdates.add(commandEntity.getTaskId());
      }
      commandEntity.setStdOut(report.getStdOut().getBytes());
      commandEntity.setStdError(report.getStdErr().getBytes());
      commandEntity.setStructuredOut(report.getStructuredOut() == null ? null :
        report.getStructuredOut().getBytes());
      commandEntity.setExitcode(report.getExitCode());

      if (HostRoleStatus.getCompletedStates().contains(commandEntity.getStatus())) {
        commandEntity.setEndTime(now);

        String actionId = report.getActionId();
        long[] requestStageIds = StageUtils.getRequestStage(actionId);
        long requestId = requestStageIds[0];
        long stageId = requestStageIds[1];
        if (requestDAO.getLastStageId(requestId).equals(stageId)) {
          requestsToCheck.add(requestId);
        }
      }
    }

    hostRoleCommandDAO.mergeAll(commandEntities);
    // Invalidate cache because of updates to ABORTED commands
    hostRoleCommandCache.invalidateAll(abortedCommandUpdates);

    for (Long requestId : requestsToCheck) {
      endRequestIfCompleted(requestId);
    }
  }

  @Override
  public void updateHostRoleState(String hostname, long requestId,
                                  long stageId, String role, CommandReport report) {
    boolean checkRequest = false;
    if (LOG.isDebugEnabled()) {
      LOG.debug("Update HostRoleState: "
        + "HostName " + hostname + " requestId " + requestId + " stageId "
        + stageId + " role " + role + " report " + report);
    }
    long now = System.currentTimeMillis();
    List<HostRoleCommandEntity> commands = hostRoleCommandDAO.findByHostRole(
      hostname, requestId, stageId, role);
    for (HostRoleCommandEntity command : commands) {
      command.setStatus(HostRoleStatus.valueOf(report.getStatus()));
      command.setStdOut(report.getStdOut().getBytes());
      command.setStdError(report.getStdErr().getBytes());
      command.setStructuredOut(report.getStructuredOut() == null ? null :
        report.getStructuredOut().getBytes());
      if (HostRoleStatus.getCompletedStates().contains(command.getStatus())) {
        command.setEndTime(now);
        if (requestDAO.getLastStageId(requestId).equals(stageId)) {
          checkRequest = true;
        }
      }
      command.setExitcode(report.getExitCode());
    }
    hostRoleCommandDAO.mergeAll(commands);

    if (checkRequest) {
      endRequestIfCompleted(requestId);
    }
  }

  @Override
  public void abortHostRole(String host, long requestId, long stageId, String role) {
    String reason = "Host Role in invalid state";
    abortHostRole(host, requestId, stageId, role, reason);
  }

  @Override
  public void abortHostRole(String host, long requestId, long stageId,
                            String role, String reason) {
    CommandReport report = new CommandReport();
    report.setExitCode(999);
    report.setStdErr(reason);
    report.setStdOut("");
    report.setStatus("ABORTED");
    updateHostRoleState(host, requestId, stageId, role, report);
  }

  @Override
  public long getLastPersistedRequestIdWhenInitialized() {
    return requestId;
  }


  @Override
  @Transactional
  public void bulkHostRoleScheduled(Stage s, List<ExecutionCommand> commands) {
    for (ExecutionCommand command : commands) {
      hostRoleScheduled(s, command.getHostname(), command.getRole());
    }
  }

  @Override
  @Transactional
  public void bulkAbortHostRole(Stage s, List<ExecutionCommand> commands) {
    for (ExecutionCommand command : commands) {
      abortHostRole(command.getHostname(), s.getRequestId(), s.getStageId(), command.getRole());
    }
  }

  @Override
  @Transactional
  public void hostRoleScheduled(Stage s, String hostname, String roleStr) {
    HostRoleCommand hostRoleCommand = s.getHostRoleCommand(hostname, roleStr);
    HostRoleCommandEntity entity = hostRoleCommandDAO.findByPK(hostRoleCommand.getTaskId());
    if (entity != null) {
      entity.setStartTime(hostRoleCommand.getStartTime());
      entity.setLastAttemptTime(hostRoleCommand.getLastAttemptTime());
      entity.setStatus(hostRoleCommand.getStatus());
      entity.setAttemptCount(hostRoleCommand.getAttemptCount());
      hostRoleCommandDAO.merge(entity);
    } else {
      throw new RuntimeException("HostRoleCommand is not persisted, cannot update:\n" + hostRoleCommand);
    }
  }

  @Override
  public List<HostRoleCommand> getRequestTasks(long requestId) {
    List<HostRoleCommand> tasks = new ArrayList<HostRoleCommand>();
    return getTasks(
        hostRoleCommandDAO.findTaskIdsByRequest(requestId)
    );
  }

  @Override
  public List<HostRoleCommand> getAllTasksByRequestIds(Collection<Long> requestIds) {
    if (requestIds.isEmpty()) {
      return Collections.emptyList();
    }

    return getTasks(
        hostRoleCommandDAO.findTaskIdsByRequestIds(requestIds)
    );
  }

  @Override
  public List<HostRoleCommand> getTasksByRequestAndTaskIds(Collection<Long> requestIds, Collection<Long> taskIds) {
    if (!requestIds.isEmpty() && !taskIds.isEmpty()) {
      return getTasks(hostRoleCommandDAO.findTaskIdsByRequestAndTaskIds(requestIds, taskIds));

    } else if (requestIds.isEmpty()) {
      return getTasks(taskIds);
    } else if (taskIds.isEmpty()) {
      return getAllTasksByRequestIds(requestIds);
    } else {
      return Collections.emptyList();
    }
  }

  @Override
  public List<HostRoleCommand> getTasks(Collection<Long> taskIds) {
    if (taskIds.isEmpty()) {
      return Collections.emptyList();
    }

    List<HostRoleCommand> commands = new ArrayList<HostRoleCommand>();

    Map<Long, HostRoleCommand> cached = hostRoleCommandCache.getAllPresent(taskIds);
    commands.addAll(cached.values());

    List<Long> absent = new ArrayList<Long>();
    absent.addAll(taskIds);
    absent.removeAll(cached.keySet());

    if (!absent.isEmpty()) {
      boolean allowStore = hostRoleCommandCache.size() <= cacheLimit;

      for (HostRoleCommandEntity commandEntity : hostRoleCommandDAO.findByPKs(absent)) {
        HostRoleCommand hostRoleCommand = hostRoleCommandFactory.createExisting(commandEntity);
        commands.add(hostRoleCommand);
        if (allowStore) {
          switch (hostRoleCommand.getStatus()) {
            case ABORTED:
            case COMPLETED:
            case TIMEDOUT:
            case FAILED:
              hostRoleCommandCache.put(hostRoleCommand.getTaskId(), hostRoleCommand);
              break;
          }
        }
      }
    }
    Collections.sort(commands, new Comparator<HostRoleCommand>() {
      @Override
      public int compare(HostRoleCommand o1, HostRoleCommand o2) {
        return (int) (o1.getTaskId()-o2.getTaskId());
      }
    });
    return commands;
  }

  @Override
  public HostRoleCommand getTask(long taskId) {
    HostRoleCommandEntity commandEntity = hostRoleCommandDAO.findByPK((int) taskId);
    if (commandEntity == null) {
      return null;
    }
    return hostRoleCommandFactory.createExisting(commandEntity);
  }

  @Override
  public List<Long> getRequestsByStatus(RequestStatus status, int maxResults,
    boolean ascOrder) {

    boolean match = true;
    boolean checkAllTasks = false;
    Set<HostRoleStatus> statuses = new HashSet<HostRoleStatus>();
    if (status == RequestStatus.IN_PROGRESS) {
      statuses.addAll(Arrays.asList(HostRoleStatus.PENDING,
          HostRoleStatus.IN_PROGRESS, HostRoleStatus.QUEUED));
    } else if (status == RequestStatus.COMPLETED) {
      match = false;
      checkAllTasks = true;
      statuses.addAll(Arrays.asList(HostRoleStatus.PENDING,
          HostRoleStatus.IN_PROGRESS, HostRoleStatus.QUEUED,
          HostRoleStatus.ABORTED, HostRoleStatus.FAILED,
          HostRoleStatus.TIMEDOUT));
    } else if (status == RequestStatus.FAILED) {
      statuses.addAll(Arrays.asList(HostRoleStatus.ABORTED,
          HostRoleStatus.FAILED, HostRoleStatus.TIMEDOUT));
    }
    return hostRoleCommandDAO.getRequestsByTaskStatus(statuses, match,
      checkAllTasks, maxResults, ascOrder);
  }

  @Override
  public Map<Long, String> getRequestContext(List<Long> requestIds) {
    return stageDAO.findRequestContext(requestIds);
  }

  @Override
  public String getRequestContext(long requestId) {
    return stageDAO.findRequestContext(requestId);
  }

  @Override
  public List<Request> getRequests(Collection<Long> requestIds){
    List<RequestEntity> requestEntities = requestDAO.findByPks(requestIds);
    List<Request> requests = new ArrayList<Request>(requestEntities.size());
    for (RequestEntity requestEntity : requestEntities) {
      requests.add(requestFactory.createExisting(requestEntity));
    }
    return requests;
  }
}
