package org.apache.ambari.server.controller.license;

/**
 * Created by jerryjzhang on 15-6-15.
 */
public class LicenseInfo {
    private String customerName;
    private int clusterLimit;

    public LicenseInfo(){
    }

    public LicenseInfo(String customerName, int clusterLimit) {
        this.customerName = customerName;
        this.clusterLimit = clusterLimit;
    }

    public LicenseInfo(String objStr){
        if(objStr != null && objStr.contains("-")){
            String [] items = objStr.split("-");
            if(items.length == 2){
                this.customerName = items[0];
                this.clusterLimit = Integer.valueOf(items[1]);
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

    @Override
    public String toString() {
        return customerName + "-" + clusterLimit;
    }
}
