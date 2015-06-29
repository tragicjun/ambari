package org.apache.ambari.server.controller.license;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.orm.dao.KeyValueDAO;
import org.apache.ambari.server.orm.entities.KeyValueEntity;

import java.util.Date;

/**
 * Created by jerryjzhang on 15-6-11.
 */
public class LicenseManager {
    protected static KeyValueDAO keyValueDAO;
    private static int DEFAULT_CLUSTER_LIMIT = 3;
    private static int DEFAULT_EXPIRATION_BY_YEAR = 1;

    public static String LICENSE_KEY = "license.key";

    public static void init(KeyValueDAO instance){
        keyValueDAO = instance;
    }

    public int getClusterLimit(){
        int limit = DEFAULT_CLUSTER_LIMIT;
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
        date.setYear(date.getYear() + DEFAULT_EXPIRATION_BY_YEAR);
        if(keyValueDAO != null){
            KeyValueEntity entity = keyValueDAO.findByKey(LICENSE_KEY);
            if(entity != null){
                LicenseInfo license = decodeLicenseKey(entity.getValue().replace("-", ""));
                date = license.getExpirationDate();
            }
        }
        return date;
    }

    public LicenseInfo getLicense(){
        LicenseInfo license = null;
        try{
            if(keyValueDAO != null){
                KeyValueEntity entity = keyValueDAO.findByKey(LICENSE_KEY);
                if(entity != null){
                    license = decodeLicenseKey(entity.getValue().replace("-", ""));
                    license.setKey(entity.getValue());
                }
            }
        }catch(Exception e){
            license = null;
        }

        return license;
    }

    public void saveLicenseKey(String licenseKey)throws AmbariException{
        LicenseInfo license = null;
        try{
            license = decodeLicenseKey(licenseKey.replace("-", ""));
        }catch(Exception e){
            license = null;
        }

        if(license == null || license.getCustomerName() == null
                || license.getExpirationDate() == null
                || license.getClusterLimit() == 0){
            throw new AmbariException("Invalid license key!");
        }

        Date now = new Date();
        if(now.after(license.getExpirationDate())){
            throw new AmbariException("License has expired!");
        }

        KeyValueEntity keyValueEntity = keyValueDAO.findByKey(LICENSE_KEY);
        if (keyValueEntity != null) {
            keyValueEntity.setValue(licenseKey);
            keyValueDAO.merge(keyValueEntity);
        } else {
            keyValueEntity = new KeyValueEntity();
            keyValueEntity.setKey(LICENSE_KEY);
            keyValueEntity.setValue(licenseKey);
            keyValueDAO.create(keyValueEntity);
        }
    }

    private LicenseInfo decodeLicenseKey(String key) {
        return new LicenseInfo(LicenseKeyConverter.decrypt(key));
    }
}
