package org.apache.ambari.server.controller;

import org.apache.ambari.server.orm.dao.KeyValueDAO;

/**
 * Created by jerryjzhang on 15-6-11.
 */
public class LicenseManager {
    protected static KeyValueDAO keyValueDAO;

    public static void init(KeyValueDAO instance){
        keyValueDAO = instance;
    }

    public int getClusterLimit(){
        return 1;
    }
}
