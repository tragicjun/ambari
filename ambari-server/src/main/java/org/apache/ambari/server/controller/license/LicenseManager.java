package org.apache.ambari.server.controller.license;

import org.apache.ambari.server.orm.dao.KeyValueDAO;
import org.apache.ambari.server.orm.entities.KeyValueEntity;

import java.util.Date;

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
                LicenseInfo license = decodeLicenseKey(entity.getValue().replace("-", ""));
                limit = license.getClusterLimit();
            }
        }
        return limit;
    }

    public Date getExpirationDate(){
        Date date = new Date();
        date.setYear(date.getYear() + 1);
        if(keyValueDAO != null){
            KeyValueEntity entity = keyValueDAO.findByKey(LICENSE_KEY);
            if(entity != null){
                LicenseInfo license = decodeLicenseKey(entity.getValue().replace("-", ""));
                date = license.getExpirationDate();
            }
        }
        return date;
    }

    private LicenseInfo decodeLicenseKey(String key) {
        return new LicenseInfo(LicenseKeyConverter.decrypt(key));
    }
}
