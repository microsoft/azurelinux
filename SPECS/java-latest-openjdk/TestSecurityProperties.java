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
    private static final String JAVA_HOME = System.getProperty("java.home");
    // JDK 11
    private static final String JDK_PROPS_FILE_JDK_11 = JAVA_HOME + "/conf/security/java.security";
    // JDK 8
    private static final String JDK_PROPS_FILE_JDK_8 = JAVA_HOME + "/lib/security/java.security";
    // JDK 25
    // Omit fips.properties files since they are not relevant to this test.
    // Omit JAVA_HOME + "/conf/security/redhat/crypto-policies.properties" which simply includes
    // true/crypto-policies.properties in case redhat.crypto-policies is left undefined.
    private static final String[] JDK_PROPS_FILES_JDK_25_ENABLED = {
            JAVA_HOME + "/conf/security/redhat/true/crypto-policies.properties",
            "/etc/crypto-policies/back-ends/java.config"
    };
    private static final String[] JDK_PROPS_FILES_JDK_25_DISABLED = {
            JAVA_HOME + "/conf/security/redhat/false/crypto-policies.properties"
    };

    private static final String POLICY_FILE = "/etc/crypto-policies/back-ends/java.config";

    private static final String MSG_PREFIX = "DEBUG: ";

    private static final String javaVersion = System.getProperty("java.version");

    // float for java 1.8
    private static final float JAVA_FEATURE = Float.parseFloat(System.getProperty("java.specification.version"));

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
        loadProperties(jdkProps, enabled);
        if (enabled) {
            loadPolicy(jdkProps);
        }
        for (Object key : jdkProps.keySet()) {
            String sKey = (String) key;
            if (JAVA_FEATURE >= 25 && sKey.equals("include")) {
                // Avoid the following exception on 25: IllegalArgumentException: Key 'include' is
                // reserved and cannot be used as a Security property name.  Hard-code the includes
                // in JDK_PROPS_FILES_JDK_25_ENABLED and JDK_PROPS_FILES_JDK_25_DISABLED instead.
                continue;
            }
            System.out.println(MSG_PREFIX + "Checking " + sKey);
            String securityVal = Security.getProperty(sKey);
            String jdkSecVal = jdkProps.getProperty(sKey);
            if (!jdkSecVal.equals(securityVal)) {
                String msg = "Expected value '" + jdkSecVal + "' for key '" +
                        sKey + "'" + " but got value '" + securityVal + "'";
                throw new RuntimeException("Test failed! " + msg);
            } else {
                System.out.println(MSG_PREFIX + sKey + " = " + jdkSecVal + " as expected.");
            }
        }
        System.out.println("TestSecurityProperties PASSED!");
    }

    private static void loadPropertiesFile(Properties props, String propsFile) {
        try (FileInputStream fin = new FileInputStream(propsFile)) {
            props.load(fin);
        } catch (Exception e) {
            throw new RuntimeException("Test failed!", e);
        }
    }

    private static void loadProperties(Properties props, boolean enabled) {
        System.out.println(MSG_PREFIX + "Java version is " + javaVersion);
        String propsFile = JDK_PROPS_FILE_JDK_11;
        if (javaVersion.startsWith("1.8.0")) {
            propsFile = JDK_PROPS_FILE_JDK_8;
        }
        loadPropertiesFile(props, propsFile);
        if (JAVA_FEATURE >= 25) {
            for (String file : enabled ? JDK_PROPS_FILES_JDK_25_ENABLED : JDK_PROPS_FILES_JDK_25_DISABLED) {
                System.out.println(MSG_PREFIX + "Loading " + file);
                loadPropertiesFile(props, file);
            }
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

/*
 * Local Variables:
 * compile-command: "\
 * /usr/lib/jvm/java-25-openjdk/bin/javac TestSecurityProperties.java \
 * && (/usr/lib/jvm/java-25-openjdk/bin/java                                TestSecurityProperties false ; [[ $? == 1 ]]) \
 * && (/usr/lib/jvm/java-25-openjdk/bin/java -Dredhat.crypto-policies=true  TestSecurityProperties false ; [[ $? == 1 ]]) \
 * && (/usr/lib/jvm/java-25-openjdk/bin/java -Dredhat.crypto-policies=false TestSecurityProperties true  ; [[ $? == 1 ]]) \
 * &&  /usr/lib/jvm/java-25-openjdk/bin/java                                TestSecurityProperties true                   \
 * &&  /usr/lib/jvm/java-25-openjdk/bin/java -Dredhat.crypto-policies=true  TestSecurityProperties true                   \
 * &&  /usr/lib/jvm/java-25-openjdk/bin/java -Dredhat.crypto-policies=false TestSecurityProperties false"                 \
 * fill-column: 124
 * End:
 */
