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

package org.apache.ambari.server.state.cluster;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

import javax.persistence.RollbackException;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.ClusterNotFoundException;
import org.apache.ambari.server.DuplicateResourceException;
import org.apache.ambari.server.HostNotFoundException;
import org.apache.ambari.server.agent.DiskInfo;
import org.apache.ambari.server.api.services.AmbariMetaInfo;
import org.apache.ambari.server.configuration.Configuration;
import org.apache.ambari.server.events.HostAddedEvent;
import org.apache.ambari.server.events.HostRegisteredEvent;
import org.apache.ambari.server.events.HostRemovedEvent;
import org.apache.ambari.server.events.publishers.AmbariEventPublisher;
import org.apache.ambari.server.orm.dao.ClusterDAO;
import org.apache.ambari.server.orm.dao.ClusterVersionDAO;
import org.apache.ambari.server.orm.dao.HostDAO;
import org.apache.ambari.server.orm.dao.HostVersionDAO;
import org.apache.ambari.server.orm.dao.KerberosPrincipalHostDAO;
import org.apache.ambari.server.orm.dao.ResourceTypeDAO;
import org.apache.ambari.server.orm.entities.ClusterEntity;
import org.apache.ambari.server.orm.entities.ClusterVersionEntity;
import org.apache.ambari.server.orm.entities.HostEntity;
import org.apache.ambari.server.orm.entities.HostVersionEntity;
import org.apache.ambari.server.orm.entities.PermissionEntity;
import org.apache.ambari.server.orm.entities.PrivilegeEntity;
import org.apache.ambari.server.orm.entities.ResourceEntity;
import org.apache.ambari.server.orm.entities.ResourceTypeEntity;
import org.apache.ambari.server.security.SecurityHelper;
import org.apache.ambari.server.security.authorization.AmbariGrantedAuthority;
import org.apache.ambari.server.state.AgentVersion;
import org.apache.ambari.server.state.Cluster;
import org.apache.ambari.server.state.Clusters;
import org.apache.ambari.server.state.Host;
import org.apache.ambari.server.state.HostHealthStatus;
import org.apache.ambari.server.state.HostHealthStatus.HealthStatus;
import org.apache.ambari.server.state.HostState;
import org.apache.ambari.server.state.RepositoryInfo;
import org.apache.ambari.server.state.StackId;
import org.apache.ambari.server.state.configgroup.ConfigGroup;
import org.apache.ambari.server.state.host.HostFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.GrantedAuthority;

import com.google.gson.Gson;
import com.google.inject.Inject;
import com.google.inject.Singleton;
import com.google.inject.persist.Transactional;

@Singleton
public class ClustersImpl implements Clusters {

  private static final Logger LOG = LoggerFactory.getLogger(
      ClustersImpl.class);

  private ConcurrentHashMap<String, Cluster> clusters;
  private ConcurrentHashMap<Long, Cluster> clustersById;
  private ConcurrentHashMap<String, Host> hosts;
  private ConcurrentHashMap<String, Set<Cluster>> hostClusterMap;
  private ConcurrentHashMap<String, Set<Host>> clusterHostMap;

  private final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
  private final Lock r = rwl.readLock();
  private final Lock w = rwl.writeLock();

  private volatile boolean clustersLoaded = false;

  @Inject
  ClusterDAO clusterDAO;
  @Inject
  HostDAO hostDAO;
  @Inject
  ClusterVersionDAO clusterVersionDAO;
  @Inject
  HostVersionDAO hostVersionDAO;
  @Inject
  ResourceTypeDAO resourceTypeDAO;
  @Inject
  KerberosPrincipalHostDAO kerberosPrincipalHostDAO;
  @Inject
  ClusterFactory clusterFactory;
  @Inject
  HostFactory hostFactory;
  @Inject
  Configuration configuration;
  @Inject
  AmbariMetaInfo ambariMetaInfo;
  @Inject
  Gson gson;
  @Inject
  private SecurityHelper securityHelper;

  /**
   * Used to publish events relating to cluster CRUD operations.
   */
  @Inject
  private AmbariEventPublisher eventPublisher;

  @Inject
  public ClustersImpl() {
    clusters = new ConcurrentHashMap<String, Cluster>();
    clustersById = new ConcurrentHashMap<Long, Cluster>();
    hosts = new ConcurrentHashMap<String, Host>();
    hostClusterMap = new ConcurrentHashMap<String, Set<Cluster>>();
    clusterHostMap = new ConcurrentHashMap<String, Set<Host>>();

    LOG.info("Initializing the ClustersImpl");
  }

  private void checkLoaded() {
    if (clustersLoaded) {
      return;
    }

    w.lock();
    try {
      if (!clustersLoaded) {
        loadClustersAndHosts();
      }
      clustersLoaded = true;
    } finally {
      w.unlock();
    }
  }

  @Transactional
  private void loadClustersAndHosts() {
    for (ClusterEntity clusterEntity : clusterDAO.findAll()) {
      Cluster currentCluster = clusterFactory.create(clusterEntity);
      clusters.put(clusterEntity.getClusterName(), currentCluster);
      clustersById.put(currentCluster.getClusterId(), currentCluster);
      clusterHostMap.put(currentCluster.getClusterName(), Collections.newSetFromMap(new ConcurrentHashMap<Host, Boolean>()));
    }

    for (HostEntity hostEntity : hostDAO.findAll()) {
      Host host = hostFactory.create(hostEntity, true);
      hosts.put(hostEntity.getHostName(), host);
      Set<Cluster> cSet = Collections.newSetFromMap(new ConcurrentHashMap<Cluster, Boolean>());
      hostClusterMap.put(hostEntity.getHostName(), cSet);

      for (ClusterEntity clusterEntity : hostEntity.getClusterEntities()) {
        clusterHostMap.get(clusterEntity.getClusterName()).add(host);
        cSet.add(clusters.get(clusterEntity.getClusterName()));
      }
    }
  }

  @Override
  public void addCluster(String clusterName)
      throws AmbariException {
    checkLoaded();

    w.lock();
    try {
      if (clusters.containsKey(clusterName)) {
        throw new DuplicateResourceException("Attempted to create a Cluster which already exists"
            + ", clusterName=" + clusterName);
      }

      // create an admin resource to represent this cluster
      ResourceTypeEntity resourceTypeEntity = resourceTypeDAO.findById(ResourceTypeEntity.CLUSTER_RESOURCE_TYPE);
      if (resourceTypeEntity == null) {
        resourceTypeEntity = new ResourceTypeEntity();
        resourceTypeEntity.setId(ResourceTypeEntity.CLUSTER_RESOURCE_TYPE);
        resourceTypeEntity.setName(ResourceTypeEntity.CLUSTER_RESOURCE_TYPE_NAME);
        resourceTypeEntity = resourceTypeDAO.merge(resourceTypeEntity);
      }

      ResourceEntity resourceEntity = new ResourceEntity();
      resourceEntity.setResourceType(resourceTypeEntity);

      // retrieve new cluster id
      // add cluster id -> cluster mapping into clustersById
      ClusterEntity clusterEntity = new ClusterEntity();
      clusterEntity.setClusterName(clusterName);
      clusterEntity.setDesiredStackVersion(gson.toJson(new StackId()));
      clusterEntity.setResource(resourceEntity);

      try {
        clusterDAO.create(clusterEntity);
        clusterEntity = clusterDAO.merge(clusterEntity);
      } catch (RollbackException e) {
        LOG.warn("Unable to create cluster " + clusterName, e);
        throw new AmbariException("Unable to create cluster " + clusterName, e);
      }

      Cluster cluster = clusterFactory.create(clusterEntity);
      clusters.put(clusterName, cluster);
      clustersById.put(cluster.getClusterId(), cluster);
      clusterHostMap.put(clusterName, new HashSet<Host>());
    } finally {
      w.unlock();
    }
  }

  @Override
  public Cluster getCluster(String clusterName)
      throws AmbariException {
    checkLoaded();
    r.lock();
    try {
      if (!clusters.containsKey(clusterName)) {
        throw new ClusterNotFoundException(clusterName);
      }
      return clusters.get(clusterName);
    } finally {
      r.unlock();
    }
  }

  @Override
  public Cluster getClusterById(long id) throws AmbariException {
    checkLoaded();
    r.lock();
    try {
      if (!clustersById.containsKey(id)) {
        throw new ClusterNotFoundException("clusterID=" + id);
      }
      return clustersById.get(id);
    } finally {
      r.unlock();
    }
  }

  @Override
  public void setCurrentStackVersion(String clusterName, StackId stackId)
      throws AmbariException{
    if(stackId == null || clusterName == null || clusterName.isEmpty()){
      LOG.warn("Unable to set version for cluster " + clusterName);
      throw new AmbariException("Unable to set"
          + " version=" + stackId
          + " for cluster " + clusterName);
    }

    checkLoaded();
    r.lock();
    try {
      if (!clusters.containsKey(clusterName)) {
        throw new ClusterNotFoundException(clusterName);
      }
      Cluster cluster = clusters.get(clusterName);
      cluster.setCurrentStackVersion(stackId);
    } finally {
      r.unlock();
    }
  }

  @Override
  public List<Host> getHosts() {
    checkLoaded();
    r.lock();

    try {
      List<Host> hostList = new ArrayList<Host>(hosts.size());
      hostList.addAll(hosts.values());
      return hostList;
    } finally {
      r.unlock();
    }
  }

  @Override
  public Set<Cluster> getClustersForHost(String hostname)
      throws AmbariException {
    checkLoaded();
    r.lock();
    try {
      if(!hostClusterMap.containsKey(hostname)){
            throw new HostNotFoundException(hostname);
      }
      if (LOG.isDebugEnabled()) {
        LOG.debug("Looking up clusters for hostname"
            + ", hostname=" + hostname
            + ", mappedClusters=" + hostClusterMap.get(hostname).size());
      }
      return Collections.unmodifiableSet(hostClusterMap.get(hostname));
    } finally {
      r.unlock();
    }
  }

  @Override
  public Host getHost(String hostname) throws AmbariException {
    checkLoaded();
    r.lock();
    try {
      if (!hosts.containsKey(hostname)) {
        throw new HostNotFoundException(hostname);
      }
      return hosts.get(hostname);
    } finally {
      r.unlock();
    }
  }

  /**
   * Register a host by creating a {@link HostEntity} object in the database and setting its state to
   * {@link HostState#INIT}. This does not add the host the cluster.
   * @param hostname Host to be added
   * @throws AmbariException
   */
  @Override
  public void addHost(String hostname) throws AmbariException {
    checkLoaded();

    String duplicateMessage = "Duplicate entry for Host"
        + ", hostName= " + hostname;

    if (hosts.containsKey(hostname)) {
      throw new AmbariException(duplicateMessage);
    }

    w.lock();

    try {
      HostEntity hostEntity = new HostEntity();
      hostEntity.setHostName(hostname);
      hostEntity.setClusterEntities(new ArrayList<ClusterEntity>());

      //not stored to DB
      Host host = hostFactory.create(hostEntity, false);
      host.setAgentVersion(new AgentVersion(""));
      List<DiskInfo> emptyDiskList = new ArrayList<DiskInfo>();
      host.setDisksInfo(emptyDiskList);
      host.setHealthStatus(new HostHealthStatus(HealthStatus.UNKNOWN, ""));
      host.setHostAttributes(new HashMap<String, String>());
      host.setState(HostState.INIT);
      hosts.put(hostname, host);
      hostClusterMap.put(hostname, Collections.newSetFromMap(new ConcurrentHashMap<Cluster, Boolean>()));

      if (LOG.isDebugEnabled()) {
        LOG.debug("Adding a host to Clusters"
            + ", hostname=" + hostname);
      }
    } finally {
      w.unlock();
    }

    // publish the event
    HostRegisteredEvent event = new HostRegisteredEvent(hostname);
    eventPublisher.publish(event);
  }

  private boolean isOsSupportedByClusterStack(Cluster c, Host h) throws AmbariException {
    Map<String, List<RepositoryInfo>> repos =
        ambariMetaInfo.getRepository(c.getDesiredStackVersion().getStackName(),
            c.getDesiredStackVersion().getStackVersion());
    return !(repos == null || repos.isEmpty()) && repos.containsKey(h.getOsFamily());
  }

  @Override
  public void updateHostWithClusterAndAttributes(
      Map<String, Set<String>> hostClusters,
      Map<String, Map<String, String>> hostAttributes) throws AmbariException {
    checkLoaded();
    w.lock();

    try {
      if (hostClusters != null) {
        Map<String, Host> hostMap = getHostsMap(hostClusters.keySet());
        Set<String> clusterNames = new HashSet<String>();
        for (Set<String> cSet : hostClusters.values()) {
          clusterNames.addAll(cSet);
        }

        for (String hostname : hostClusters.keySet()) {
          Host host = hostMap.get(hostname);
          Map<String, String>  attributes = hostAttributes.get(hostname);
          if (attributes != null && !attributes.isEmpty()){
            host.setHostAttributes(attributes);
          }

          host.refresh();

          Set<String> hostClusterNames = hostClusters.get(hostname);
          for (String clusterName : hostClusterNames) {
            if (clusterName != null && !clusterName.isEmpty()) {
              mapHostToCluster(hostname, clusterName);
            }
          }
        }
      }
    } finally {
      w.unlock();
    }
  }

  private Map<String, Host> getHostsMap(Collection<String> hostSet) throws
      HostNotFoundException {
    checkLoaded();
    Map<String, Host> hostMap = new HashMap<String, Host>();
    r.lock();
    try {
      for (String host : hostSet) {
        if (!hosts.containsKey(host)) {
          throw new HostNotFoundException(host);
        } else {
          hostMap.put(host, hosts.get(host));
        }
      }
    } finally {
      r.unlock();
    }
    return hostMap;
  }

  private Map<String, Cluster> getClustersMap(Collection<String> clusterSet) throws
      ClusterNotFoundException {
    checkLoaded();
    Map<String, Cluster> clusterMap = new HashMap<String, Cluster>();
    r.lock();
    try {
      for (String c : clusterSet) {
        if (c != null) {
          if (!clusters.containsKey(c)) {
            throw new ClusterNotFoundException(c);
          } else {
            clusterMap.put(c, clusters.get(c));
          }
        }
      }
    } finally {
      r.unlock();
    }
    return clusterMap;
  }

  /**
   *  For each host, attempts to map it to the cluster, and apply the cluster's current version to the host.
   * @param hostnames Collection of host names
   * @param clusterName Cluster name
   * @throws AmbariException
   */
  @Override
  public void mapHostsToCluster(Set<String> hostnames, String clusterName) throws AmbariException {
    checkLoaded();
    w.lock();
    try {
      ClusterVersionEntity clusterVersionEntity = clusterVersionDAO.findByClusterAndStateCurrent(clusterName);
      for (String hostname : hostnames) {
        mapHostToCluster(hostname, clusterName, clusterVersionEntity);
      }
    } finally {
      w.unlock();
    }
  }

  /**
   * Attempts to map the host to the cluster via clusterhostmapping table if not already present, and add a host_version
   * record for the cluster's currently applied (stack, version) if not already present.
   * @param hostname Host name
   * @param clusterName Cluster name
   * @param currentClusterVersion Cluster's current stack version
   * @throws AmbariException May throw a DuplicateResourceException.
   */
  public void mapHostToCluster(String hostname, String clusterName,
      ClusterVersionEntity currentClusterVersion) throws AmbariException {
    Host host = null;
    Cluster cluster = null;

    checkLoaded();

    r.lock();
    try {
      host = getHost(hostname);
      cluster = getCluster(clusterName);

      // check to ensure there are no duplicates
      for (Cluster c : hostClusterMap.get(hostname)) {
        if (c.getClusterName().equals(clusterName)) {
          LOG.info("Attempted to create a host which already exists: clusterName=" +
            clusterName + ", hostName=" + hostname);
          return;
//          throw new DuplicateResourceException("Attempted to create a host which already exists: clusterName=" +
//              clusterName + ", hostName=" + hostname);
        }
      }
    } finally {
      r.unlock();
    }

    if (!isOsSupportedByClusterStack(cluster, host)) {
      String message = "Trying to map host to cluster where stack does not"
          + " support host's os type" + ", clusterName=" + clusterName
          + ", clusterStackId=" + cluster.getDesiredStackVersion().getStackId()
          + ", hostname=" + hostname + ", hostOsFamily=" + host.getOsFamily();
      LOG.warn(message);
      throw new AmbariException(message);
    }

    long clusterId = cluster.getClusterId();
    if (LOG.isDebugEnabled()) {
      LOG.debug("Mapping host {} to cluster {} (id={})", hostname, clusterName,
          clusterId);
    }

    w.lock();
    try {
      mapHostClusterEntities(hostname, clusterId);
      hostClusterMap.get(hostname).add(cluster);
      clusterHostMap.get(clusterName).add(host);
    } finally {
      w.unlock();
    }

    ReadWriteLock clusterLock = cluster.getClusterGlobalLock();
    clusterLock.writeLock().lock();
    try {
      host.refresh();
      cluster.refresh();
    } finally {
      clusterLock.writeLock().unlock();
    }
  }

  /**
   * Attempts to map the host to the cluster via clusterhostmapping table if not already present, and add a host_version
   * record for the cluster's currently applied (stack, version) if not already present. This function is overloaded.
   * @param hostname Host name
   * @param clusterName Cluster name
   * @throws AmbariException May throw a DuplicateResourceException.
   */
  @Override
  public void mapHostToCluster(String hostname, String clusterName)
      throws AmbariException {
    checkLoaded();

    ClusterVersionEntity clusterVersionEntity = clusterVersionDAO.findByClusterAndStateCurrent(clusterName);
    mapHostToCluster(hostname, clusterName, clusterVersionEntity);
  }

  @Transactional
  private void mapHostClusterEntities(String hostName, Long clusterId) {
    HostEntity hostEntity = hostDAO.findByName(hostName);
    ClusterEntity clusterEntity = clusterDAO.findById(clusterId);

    hostEntity.getClusterEntities().add(clusterEntity);
    clusterEntity.getHostEntities().add(hostEntity);

    clusterDAO.merge(clusterEntity);
    hostDAO.merge(hostEntity);

    // publish the event for adding a host to a cluster
    HostAddedEvent event = new HostAddedEvent(clusterId, hostName);
    eventPublisher.publish(event);
  }

  @Override
  public Map<String, Cluster> getClusters() {
    checkLoaded();
    r.lock();
    try {
      return Collections.unmodifiableMap(clusters);
    } finally {
      r.unlock();
    }
  }

  @Override
  public void updateClusterName(String oldName, String newName) {
    w.lock();
    try {
      clusters.put(newName, clusters.remove(oldName));
      clusterHostMap.put(newName, clusterHostMap.remove(oldName));
    } finally {
      w.unlock();
    }
  }


  @Override
  public void debugDump(StringBuilder sb) {
    r.lock();
    try {
      sb.append("Clusters=[ ");
      boolean first = true;
      for (Cluster c : clusters.values()) {
        if (!first) {
          sb.append(" , ");
        }
        first = false;
        sb.append("\n  ");
        c.debugDump(sb);
        sb.append(" ");
      }
      sb.append(" ]");
    } finally {
      r.unlock();
    }
  }

  @Override
  public Map<String, Host> getHostsForCluster(String clusterName)
      throws AmbariException {

    checkLoaded();
    r.lock();

    try {
      Map<String, Host> hosts = new HashMap<String, Host>();

      for (Host h : clusterHostMap.get(clusterName)) {
        hosts.put(h.getHostName(), h);
      }

      return hosts;
    } finally {
      r.unlock();
    }
  }

  @Override
  public void deleteCluster(String clusterName)
      throws AmbariException {
    checkLoaded();
    w.lock();
    try {
      Cluster cluster = getCluster(clusterName);
      if (!cluster.canBeRemoved()) {
        throw new AmbariException("Could not delete cluster"
            + ", clusterName=" + clusterName);
      }
      LOG.info("Deleting cluster " + cluster.getClusterName());
      cluster.delete();

      //clear maps
      for (Set<Cluster> clusterSet : hostClusterMap.values()) {
        clusterSet.remove(cluster);
      }
      clusterHostMap.remove(cluster.getClusterName());

      Collection<ClusterVersionEntity> clusterVersions = cluster.getAllClusterVersions();
      for (ClusterVersionEntity clusterVersion : clusterVersions) {
        clusterVersionDAO.remove(clusterVersion);
      }

      clusters.remove(clusterName);
    } finally {
      w.unlock();
    }
  }

  @Override
  public void unmapHostFromCluster(String hostname, String clusterName)
      throws AmbariException {
    Host host = null;
    Cluster cluster = null;

    checkLoaded();

    r.lock();
    try {
      host = getHost(hostname);
      cluster = getCluster(clusterName);
    } finally {
      r.unlock();
    }

    long clusterId = cluster.getClusterId();
    if (LOG.isDebugEnabled()) {
      LOG.debug("Unmapping host {} from cluster {} (id={})", hostname,
          clusterName, clusterId);
    }

    w.lock();

    try {
      unmapHostClusterEntities(hostname, cluster.getClusterId());

      hostClusterMap.get(hostname).remove(cluster);
      clusterHostMap.get(clusterName).remove(host);

      host.refresh();
      cluster.refresh();

      deleteConfigGroupHostMapping(hostname);

      // Remove mapping of principals to the unmapped host
      kerberosPrincipalHostDAO.removeByHost(hostname);
    } finally {
      w.unlock();
    }
  }

  @Transactional
  private void unmapHostClusterEntities(String hostName, long clusterId) {
    HostEntity hostEntity = hostDAO.findByName(hostName);
    ClusterEntity clusterEntity = clusterDAO.findById(clusterId);

    hostEntity.getClusterEntities().remove(clusterEntity);
    clusterEntity.getHostEntities().remove(hostEntity);

    hostDAO.merge(hostEntity);
    clusterDAO.merge(clusterEntity);
  }

  @Transactional
  private void deleteConfigGroupHostMapping(String hostname) throws AmbariException {
    // Remove Config group mapping
    for (Cluster cluster : clusters.values()) {
      for (ConfigGroup configGroup : cluster.getConfigGroups().values()) {
        configGroup.removeHost(hostname);
      }
    }
  }

  @Override
  public void deleteHost(String hostname) throws AmbariException {
    checkLoaded();

    if (!hosts.containsKey(hostname)) {
      return;
    }

    w.lock();

    try {
      deleteConfigGroupHostMapping(hostname);

      Collection<HostVersionEntity> hostVersions = hosts.get(hostname).getAllHostVersions();
      for (HostVersionEntity hostVersion : hostVersions) {
        hostVersionDAO.remove(hostVersion);
      }

      HostEntity entity = hostDAO.findByName(hostname);
      hostDAO.refresh(entity);
      hostDAO.remove(entity);
      hosts.remove(hostname);

      // Remove mapping of principals to deleted host
      kerberosPrincipalHostDAO.removeByHost(hostname);

      // publish the event
      HostRemovedEvent event = new HostRemovedEvent(hostname);
      eventPublisher.publish(event);

    } catch (Exception e) {
      throw new AmbariException("Could not remove host", e);
    } finally {
      w.unlock();
    }

  }

  @Override
  public boolean checkPermission(String clusterName, boolean readOnly) {

    Cluster cluster = findCluster(clusterName);

    return (cluster == null && readOnly) || !configuration.getApiAuthentication()
      || checkPermission(cluster, readOnly);
  }

  @Override
  public void addSessionAttributes(String name, Map<String, Object> attributes) {
    Cluster cluster = findCluster(name);
    if (cluster != null) {
      cluster.addSessionAttributes(attributes);
    }
  }

  @Override
  public Map<String, Object> getSessionAttributes(String name) {
    Cluster cluster = findCluster(name);
    return cluster == null ? Collections.<String, Object>emptyMap() : cluster.getSessionAttributes();
  }


  // ----- helper methods ---------------------------------------------------

  /**
   * Find the cluster for the given name.
   *
   * @param name  the cluster name
   *
   * @return the cluster for the given name; null if the cluster can not be found
   */
  protected Cluster findCluster(String name) {
    Cluster cluster = null;
    try {
      cluster = name == null ? null : getCluster(name);
    } catch (AmbariException e) {
      // do nothing
    }
    return cluster;
  }

  /**
   * Determine whether or not access to the given cluster resource should be allowed based
   * on the privileges of the current user.
   *
   * @param cluster   the cluster
   * @param readOnly  indicate whether or not this check is for a read only operation
   *
   * @return true if the access to this cluster is allowed
   */
  private boolean checkPermission(Cluster cluster, boolean readOnly) {
    for (GrantedAuthority grantedAuthority : securityHelper.getCurrentAuthorities()) {
      if (grantedAuthority instanceof AmbariGrantedAuthority) {

        AmbariGrantedAuthority authority       = (AmbariGrantedAuthority) grantedAuthority;
        PrivilegeEntity        privilegeEntity = authority.getPrivilegeEntity();
        Integer                permissionId    = privilegeEntity.getPermission().getId();

        // admin has full access
        if (permissionId.equals(PermissionEntity.AMBARI_ADMIN_PERMISSION)) {
          return true;
        }
        if (cluster != null) {
          if (cluster.checkPermission(privilegeEntity, readOnly)) {
            return true;
          }
        }
      }
    }
    // TODO : should we log this?
    return false;
  }
}
