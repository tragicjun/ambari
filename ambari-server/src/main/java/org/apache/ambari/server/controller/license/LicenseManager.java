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

    public LicenseInfo getLicense(){
        LicenseInfo license = null;
        try{
            if(keyValueDAO != null){
                KeyValueEntity entity = keyValueDAO.findByKey(LICENSE_KEY);
                if(entity != null){
                    license = decodeLicenseKey(entity.getValue().replace("-", ""));
                }
            }
        }catch(Exception e){
            license = null;
        }

        return license;
    }

    public void saveLicenseKey(String licenseKey)throws AmbariException{
        boolean valid = false;
        try{
            LicenseInfo license = decodeLicenseKey(licenseKey.replace("-", ""));
            if(license != null && license.getCustomerName() != null){
                valid = true;
            }
        }catch(Exception e){
            valid = false;
        }

        if(!valid){
            throw new AmbariException("Invalid license key!");
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
