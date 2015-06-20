package org.apache.ambari.server.controller.license;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by jerryjzhang on 15-6-15.
 */
public class LicenseInfo {
    private static SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd");

    private String customerName;
    private int clusterLimit;
    private Date expirationDate;
    private String key;

    public LicenseInfo(){
    }

    public LicenseInfo(String customerName, int clusterLimit, String expirationDate) {
        this.customerName = customerName;
        this.clusterLimit = clusterLimit;
        this.expirationDate = new Date(expirationDate);
    }

    public LicenseInfo(String objStr){
        if(objStr != null && objStr.contains("-")){
            String [] items = objStr.split("-");
            if(items.length == 3){
                this.customerName = items[0];
                this.clusterLimit = Integer.valueOf(items[1]);
                this.expirationDate = new Date(items[2]);
            }
        }
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public int getClusterLimit() {
        return clusterLimit;
    }

    public void setClusterLimit(int clusterLimit) {
        this.clusterLimit = clusterLimit;
    }

    public Date getExpirationDate() {
        return expirationDate;
    }

    public void setExpirationDate(Date expirationDate) {
        this.expirationDate = expirationDate;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    @Override
    public String toString() {
        return customerName + "-" + clusterLimit + "-" + dateFormat.format(expirationDate);
    }
}
