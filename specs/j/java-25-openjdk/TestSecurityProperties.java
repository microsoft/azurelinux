/* TestSecurityProperties -- Ensure system security properties can be used to
                             enable the crypto policies.
   Copyright (C) 2022 Red Hat, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
import java.io.File;
import java.io.FileInputStream;
import java.security.Security;
import java.util.Properties;

public class TestSecurityProperties {
    // JDK 11
    private static final String JDK_PROPS_FILE_JDK_11 = System.getProperty("java.home") + "/conf/security/java.security";
    // JDK 8
    private static final String JDK_PROPS_FILE_JDK_8 = System.getProperty("java.home") + "/lib/security/java.security";

    private static final String POLICY_FILE = "/etc/crypto-policies/back-ends/java.config";

    private static final String MSG_PREFIX = "DEBUG: ";

    public static void main(String[] args) {
        if (args.length == 0) {
            System.err.println("TestSecurityProperties <true|false>");
            System.err.println("Invoke with 'true' if system security properties should be enabled.");
            System.err.println("Invoke with 'false' if system security properties should be disabled.");
            System.exit(1);
        }
        boolean enabled = Boolean.valueOf(args[0]);
        System.out.println(MSG_PREFIX + "System security properties enabled: " + enabled);
        Properties jdkProps = new Properties();
        loadProperties(jdkProps);
        if (enabled) {
            loadPolicy(jdkProps);
        }
        for (Object key: jdkProps.keySet()) {
            String sKey = (String)key;
            String securityVal = Security.getProperty(sKey);
            String jdkSecVal = jdkProps.getProperty(sKey);
            if (!securityVal.equals(jdkSecVal)) {
                String msg = "Expected value '" + jdkSecVal + "' for key '" +
                             sKey + "'" + " but got value '" + securityVal + "'";
                throw new RuntimeException("Test failed! " + msg);
            } else {
                System.out.println(MSG_PREFIX + sKey + " = " + jdkSecVal + " as expected.");
            }
        }
        System.out.println("TestSecurityProperties PASSED!");
    }

    private static void loadProperties(Properties props) {
        String javaVersion = System.getProperty("java.version");
        System.out.println(MSG_PREFIX + "Java version is " + javaVersion);
        String propsFile = JDK_PROPS_FILE_JDK_11;
        if (javaVersion.startsWith("1.8.0")) {
            propsFile = JDK_PROPS_FILE_JDK_8;
        }
        try (FileInputStream fin = new FileInputStream(propsFile)) {
            props.load(fin);
        } catch (Exception e) {
            throw new RuntimeException("Test failed!", e);
        }
    }

    private static void loadPolicy(Properties props) {
        try (FileInputStream fin = new FileInputStream(POLICY_FILE)) {
            props.load(fin);
        } catch (Exception e) {
            throw new RuntimeException("Test failed!", e);
        }
    }

}
