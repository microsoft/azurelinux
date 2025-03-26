/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.xerces.util;

import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.types.Path;
import org.apache.tools.ant.util.JavaEnvUtils;
import org.apache.tools.ant.taskdefs.Javac;

import java.lang.StringBuffer;
import java.util.Properties;
import java.util.Locale;

/**
 * The implementation of the javac compiler for JDK 1.4 and above
 *
 * The purpose of this task is to diagnose whether we're
 * running on a 1.4 or above JVM; if we are, to
 * set up the bootclasspath such that the build will
 * succeed; if we aren't, then invoke the Javac12
 * task.
 *
 * @author Neil Graham, IBM
 */
public class XJavac extends Javac {

    /**
     * Run the compilation.
     *
     * @exception BuildException if the compilation has problems.
     */
    public void execute() throws BuildException {
        Properties props = null;
        try {
            props = System.getProperties();
        } catch (Exception e) {
            throw new BuildException("unable to determine java vendor because could not access system properties!");
        }
        String currBCP = (String)props.get("sun.boot.class.path");      // this property is absent / null with JDK 9 & above
        
        if(isJDK14OrHigher() && !(currBCP == null)) {
            // maybe the right one; check vendor:
            // by checking system properties:            
            // this is supposed to be provided by all JVM's from time immemorial
            String vendor = ((String)props.get("java.vendor")).toUpperCase(Locale.ENGLISH);
            if (vendor.indexOf("IBM") >= 0) {
                // we're on an IBM 1.4 or higher; fiddle with the bootclasspath.
                setBootclasspath(createIBMJDKBootclasspath());
            }
            // need to do special things for Sun/Oracle too and also
            // for Apple, HP, FreeBSD, SableVM, Kaffe and Blackdown: a Linux port of Sun Java
            else if( (vendor.indexOf("SUN") >= 0) || 
                     (vendor.indexOf("ORACLE") >= 0) ||
                     (vendor.indexOf("BLACKDOWN") >= 0) || 
                     (vendor.indexOf("APPLE") >= 0) ||
                     (vendor.indexOf("HEWLETT-PACKARD") >= 0) ||
                     (vendor.indexOf("KAFFE") >= 0) ||
                     (vendor.indexOf("SABLE") >= 0) ||
                     (vendor.indexOf("FREEBSD") >= 0)) {
                // we're on an SUN 1.4 or higher; fiddle with the bootclasspath.
                // since we can't eviscerate XML-related info here,
                // we must use the classpath
                Path bcp = createBootclasspath();
                Path clPath = getClasspath();
                bcp.append(clPath);                
                Path currBCPath = new Path(null); 
                currBCPath.createPathElement().setPath(currBCP);
                bcp.append(currBCPath);
                setBootclasspath(bcp);
            }
        }
        // now just do the normal thing:
        super.execute();
    }
    
    /**
     * Creates bootclasspath for IBM JDK 1.4 and above.
     */
    private Path createIBMJDKBootclasspath() {
        Path bcp = createBootclasspath();
        String javaHome = System.getProperty("java.home");
        StringBuffer bcpMember = new StringBuffer();
        bcpMember.append(javaHome).append("/bin/default/jclSC170/vm.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/ppc/default/jclSC170/vm.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/charsets.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/core.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/math.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/vm.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/java.util.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(), "/lib/rt.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/graphics.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/javaws.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/jaws.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/security.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/server.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/JawBridge.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/gskikm.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/ibmjceprovider.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/indicim.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/jaccess.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/ldapsec.jar:");
        bcp.createPathElement().setPath(bcpMember.toString());
        bcpMember.replace(javaHome.length(), bcpMember.length(),  "/lib/ext/oldcertpath.jar");
        bcp.createPathElement().setPath(bcpMember.toString());
        return bcp;
    }
    
    /**
     * Checks whether the JDK version is 1.4 or higher. If it's not
     * JDK 1.4 we check whether we're on a future JDK by checking
     * that we're not on JDKs 1.0, 1.1, 1.2 or 1.3. This check by 
     * exclusion should future proof this task from new versions of 
     * Ant which are aware of higher JDK versions.
     * 
     * @return true if the JDK version is 1.4 or higher.
     */
    private boolean isJDK14OrHigher() {
        final String version = JavaEnvUtils.getJavaVersion();
        return version.equals(JavaEnvUtils.JAVA_1_4) ||
            (!version.equals(JavaEnvUtils.JAVA_1_3) &&
            !version.equals(JavaEnvUtils.JAVA_1_2) &&
            !version.equals(JavaEnvUtils.JAVA_1_1) &&
            !version.equals(JavaEnvUtils.JAVA_1_0));
    }
}
