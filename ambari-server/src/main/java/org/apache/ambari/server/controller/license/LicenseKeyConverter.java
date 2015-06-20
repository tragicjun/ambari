package org.apache.ambari.server.controller.license;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.security.Key;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.spec.AlgorithmParameterSpec;

/**
 * Created by jerryjzhang on 15-6-15.
 */
public class LicenseKeyConverter {
    public static String encrypt(String src) {
        try {
            return LicenseBase32.encode(src.getBytes());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static String decrypt(String src) {
        String decrypted = "";
        try {
            byte[] outputBuf = LicenseBase32.decode(src);
            decrypted = new String(outputBuf, "utf-8");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return decrypted;
    }
}
