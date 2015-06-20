package org.apache.ambari.server.api.services;

import org.apache.ambari.server.AmbariException;
import org.apache.ambari.server.controller.AmbariServer;
import org.apache.ambari.server.controller.license.LicenseInfo;
import org.apache.ambari.server.controller.license.LicenseManager;

import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Response;

/**
 * Created by jerryjzhang on 2015/6/20.
 */
@Path("/license/")
public class LicenseService {
    @SuppressWarnings("unchecked")
    @GET
    @Produces("application/json")
    public Response getLicense(){
        LicenseManager licenseManager = AmbariServer.getController().getLicenseManager();
        LicenseInfo license = licenseManager.getLicense();
        if(license != null){
            return Response.ok(license).build();
        }else{
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }

    @SuppressWarnings("unchecked")
    @POST
    @Produces("application/json")
    public Response saveLicenseKey(String key){
        LicenseManager licenseManager = AmbariServer.getController().getLicenseManager();
        try {
            licenseManager.saveLicenseKey(key);
        }catch(AmbariException e){
            return Response.status(Response.Status.BAD_REQUEST).build();
        }

        return Response.status(Response.Status.CREATED).build();
    }

}
