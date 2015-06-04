package org.apache.ambari.server.audit;

import org.apache.ambari.server.api.services.Request;

import javax.ws.rs.core.Response;

/**
 * Created by Administrator on 2015/5/15.
 */
public class DatabaseAuditor extends Auditor {
  /**
   * Set a mark
   */
  @Override
  public void mark() {

  }

  /**
   * Record audit message to database
   *
   * @param message
   */
  @Override
  public void record(String message) {

  }

  /**
   * Record api request and response
   *
   * @param request
   * @param response
   */
  @Override
  public void record(Request request, Response response) {

  }
}
