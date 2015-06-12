package org.apache.ambari.server.controller;

import org.apache.ambari.server.orm.dao.KeyValueDAO;
import org.apache.ambari.server.orm.entities.KeyValueEntity;

/**
 * Created by jerryjzhang on 15-6-11.
 */
public class LicenseManager {
    protected static KeyValueDAO keyValueDAO;
    public static String LICENSE_KEY = "license.key";

    public static void init(KeyValueDAO instance){
        keyValueDAO = instance;
    }

    public int getClusterLimit(){
        int limit = 1;
        if(keyValueDAO != null){
            KeyValueEntity entity = keyValueDAO.findByKey(LICENSE_KEY);
            if(entity != null){
                limit = decodeLicenseKey(entity.getValue());
            }
        }
        return limit;
    }

    private int decodeLicenseKey(String key){
        return Integer.valueOf(key);
    }
}
