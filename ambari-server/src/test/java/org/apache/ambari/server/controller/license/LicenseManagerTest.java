package org.apache.ambari.server.controller.license;

import junit.framework.Assert;
import org.apache.ambari.server.orm.dao.KeyValueDAO;
import org.apache.ambari.server.orm.entities.KeyValueEntity;
import org.easymock.EasyMock;
import org.junit.Before;
import org.junit.Test;

import java.util.Date;

/**
 * Created by jerryjzhang on 15-6-15.
 */
public class LicenseManagerTest {
    private LicenseManager licenseManager;
    private LicenseInfo licenseInfo;

    @Before
    public void setUp(){
        licenseInfo = new LicenseInfo("jerryjzhang", 100, "2015/06/20");
        String licenseKey = LicenseKeyConverter.encrypt(licenseInfo.toString());

        KeyValueEntity keyValueEntity = new KeyValueEntity();
        keyValueEntity.setKey(LicenseManager.LICENSE_KEY);
        keyValueEntity.setValue(licenseKey);

        KeyValueDAO mockDao = EasyMock.createMock(KeyValueDAO.class);
        EasyMock.expect(mockDao.findByKey(LicenseManager.LICENSE_KEY)).andReturn(keyValueEntity);
        EasyMock.expect(mockDao.findByKey(LicenseManager.LICENSE_KEY)).andReturn(keyValueEntity);
        EasyMock.replay(mockDao);

        LicenseManager.init(mockDao);
        licenseManager = new LicenseManager();
    }

    @Test
    public void testGetClusterLimit(){
        int limit = licenseManager.getClusterLimit();
        Date date = licenseManager.getExpirationDate();
        Assert.assertEquals(licenseInfo.getClusterLimit(), limit);
        Assert.assertEquals(licenseInfo.getExpirationDate(), date);
    }
}
