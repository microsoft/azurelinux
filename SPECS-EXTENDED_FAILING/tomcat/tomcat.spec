Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global jspspec 2.3
%global major_version 9
%global minor_version 0
%global micro_version 39
%global packdname apache-tomcat-%{version}-src
%global servletspec 4.0
%global elspec 3.0
%global tcuid 53
# Recommended version is specified in java/org/apache/catalina/core/AprLifecycleListener.java
%global native_version 1.2.21


# FHS 2.3 compliant tree structure - http://www.pathname.com/fhs/2.3/
%global basedir %{_var}/lib/%{name}
%global appdir %{basedir}/webapps
%global homedir %{_datadir}/%{name}
%global bindir %{homedir}/bin
%global confdir %{_sysconfdir}/%{name}
%global libdir %{_javadir}/%{name}
%global logdir %{_var}/log/%{name}
%global cachedir %{_var}/cache/%{name}
%global tempdir %{cachedir}/temp
%global workdir %{cachedir}/work
%global _systemddir /lib/systemd/system

# Fedora doesn't seem to have this macro, so we define it if it doesn't exist
%{!?_mavendepmapfragdir: %global _mavendepmapfragdir /usr/share/maven-metadata}

Name:          tomcat
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       6%{?dist}
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

License:       ASL 2.0
URL:           http://tomcat.apache.org/
Source0:       https://archive.apache.org/dist/%{name}/%{name}-%{major_version}/v%{version}/src/%{packdname}.tar.gz
Source1:       %{name}-%{major_version}.%{minor_version}.conf
Source3:       %{name}-%{major_version}.%{minor_version}.sysconfig
Source4:       %{name}-%{major_version}.%{minor_version}.wrapper
Source5:       %{name}-%{major_version}.%{minor_version}.logrotate
Source6:       %{name}-%{major_version}.%{minor_version}-digest.script
Source7:       %{name}-%{major_version}.%{minor_version}-tool-wrapper.script
Source11:      %{name}-%{major_version}.%{minor_version}.service
Source20:      %{name}-%{major_version}.%{minor_version}-jsvc.service
Source21:      tomcat-functions
Source30:      tomcat-preamble
Source31:      tomcat-server
Source32:      tomcat-named.service

Patch0:        %{name}-%{major_version}.%{minor_version}-bootstrap-MANIFEST.MF.patch
Patch1:        %{name}-%{major_version}.%{minor_version}-tomcat-users-webapp.patch
Patch2:        %{name}-build.patch
Patch3:        change-defaults-for-CVE-2020-1938.patch
Patch4:        %{name}-%{major_version}.%{minor_version}-catalina-policy.patch
Patch5:        rhbz-1857043.patch
Patch6:        %{name}-%{major_version}.%{minor_version}-LogFactory.patch
Patch7:        concurrency-issue-for-CVE-2020-17527.patch

BuildArch:     noarch

BuildRequires: ant
BuildRequires: ecj >= 4.10
BuildRequires: findutils
BuildRequires: apache-commons-daemon
BuildRequires: tomcat-taglibs-standard
BuildRequires: java-devel >= 1.8.0

# add_maven_depmap is deprecated, using javapackages-local for now
# See https://fedora-java.github.io/howto/latest/#_add_maven_depmap_macro
BuildRequires: javapackages-local

BuildRequires: geronimo-jaxrpc
BuildRequires: geronimo-saaj
BuildRequires: aqute-bnd
BuildRequires: aqute-bndlib
BuildRequires: wsdl4j
BuildRequires: systemd

Requires:      apache-commons-daemon
Requires:      java >= 1.8.0
Requires:      javapackages-tools
Requires:      procps
Requires:      %{name}-lib = %{version}-%{release}
Recommends:    tomcat-native >= %{native_version}
Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

# added after log4j sub-package was removed
Provides:         %{name}-log4j = %{version}-%{release}

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%package admin-webapps
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package jsvc
Summary: Apache jsvc wrapper for Apache Tomcat as separate service
Requires: %{name} = %{version}-%{release}
Requires: apache-commons-daemon-jsvc

%description jsvc
Systemd service to start tomcat with jsvc,
which allows tomcat to perform some privileged operations
(e.g. bind to a port < 1024) and then switch identity to a non-privileged user.

%package jsp-%{jspspec}-api
Summary: Apache Tomcat JavaServer Pages v%{jspspec} API Implementation Classes
Provides: jsp = %{jspspec}
Obsoletes: %{name}-jsp-2.2-api
Requires: %{name}-servlet-%{servletspec}-api = %{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{version}-%{release}

%description jsp-%{jspspec}-api
Apache Tomcat JSP API Implementation Classes.

%package lib
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name}-jsp-%{jspspec}-api = %{version}-%{release}
Requires: %{name}-servlet-%{servletspec}-api = %{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{version}-%{release}
Requires: ecj >= 4.10
Requires(preun): coreutils

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Summary: Apache Tomcat Java Servlet v%{servletspec} API Implementation Classes
Provides: servlet = %{servletspec}
Provides: servlet6
Provides: servlet3
Obsoletes: %{name}-servlet-3.1-api

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API Implementation Classes.

%package el-%{elspec}-api
Summary: Apache Tomcat Expression Language v%{elspec} API Implementation Classes
Provides: el_api = %{elspec}
Obsoletes: %{name}-el-2.2-api

%description el-%{elspec}-api
Apache Tomcat EL API Implementation Classes.

%package webapps
Summary: The ROOT and examples web applications for Apache Tomcat
Requires: %{name} = %{version}-%{release}
Requires: tomcat-taglibs-standard >= 1.1

%description webapps
The ROOT and examples web applications for Apache Tomcat.

%prep
%setup -q -n %{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0

%{__ln_s} $(build-classpath tomcat-taglibs-standard/taglibs-standard-impl) webapps/examples/WEB-INF/lib/jstl.jar
%{__ln_s} $(build-classpath tomcat-taglibs-standard/taglibs-standard-compat) webapps/examples/WEB-INF/lib/standard.jar

%build
export OPT_JAR_LIST="xalan-j2-serializer"
   # we don't care about the tarballs and we're going to replace
   # tomcat-dbcp.jar with apache-commons-{collections,dbcp,pool}-tomcat5.jar
   # so just create a dummy file for later removal
   touch HACK

   # who needs a build.properties file anyway
   %{ant} -Dbase.path="." \
      -Dbuild.compiler="modern" \
      -Dcommons-daemon.jar="$(build-classpath apache-commons-daemon)" \
      -Dcommons-daemon.native.src.tgz="HACK" \
      -Djdt.jar="$(build-classpath ecj/ecj)" \
      -Dtomcat-native.tar.gz="HACK" \
      -Dtomcat-native.home="." \
      -Dcommons-daemon.native.win.mgr.exe="HACK" \
      -Dnsis.exe="HACK" \
      -Djaxrpc-lib.jar="$(build-classpath jaxrpc)" \
      -Dwsdl4j-lib.jar="$(build-classpath wsdl4j)" \
      -Dsaaj-api.jar="$(build-classpath geronimo-saaj)" \
      -Dbnd.jar="$(build-classpath aqute-bnd/biz.aQute.bnd)" \
      -Dbndlib.jar="$(build-classpath aqute-bnd/biz.aQute.bndlib)" \
      -Dbndlibg.jar="$(build-classpath aqute-bnd/aQute.libg)" \
      -Dbndannotation.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
      -Dosgi-annotations.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
      -Dslf4j-api.jar="$(build-classpath slf4j/slf4j-api)" \
      -Dosgi-cmpn.jar="$(build-classpath osgi-compendium/osgi.cmpn)" \
      -Dversion="%{version}" \
      -Dversion.build="%{micro_version}" \
      deploy dist-source

    # remove some jars that we'll replace with symlinks later
    %{__rm} output/build/bin/commons-daemon.jar output/build/lib/ecj.jar
pushd output/dist/src/webapps/docs/appdev/sample/src
%{__mkdir_p} ../web/WEB-INF/classes
%{javac} -cp ../../../../../../../../output/build/lib/servlet-api.jar -d ../web/WEB-INF/classes mypackage/Hello.java
pushd ../web
%{jar} cf ../../../../../../../../output/build/webapps/docs/appdev/sample/sample.war *
popd
popd

%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_systemddir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{appdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{bindir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > ${RPM_BUILD_ROOT}%{confdir}/conf.d/README
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{libdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{logdir}
/bin/touch ${RPM_BUILD_ROOT}%{logdir}/catalina.out
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{_localstatedir}/lib/tomcats
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{homedir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{tempdir}
%{__install} -d -m 0775 ${RPM_BUILD_ROOT}%{workdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_unitdir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}

# move things into place
# First copy supporting libs to tomcat lib
pushd output/build
    %{__cp} -a bin/*.{jar,xml} ${RPM_BUILD_ROOT}%{bindir}
    %{__cp} -a conf/*.{policy,properties,xml,xsd} ${RPM_BUILD_ROOT}%{confdir}
    %{__cp} -a lib/*.jar ${RPM_BUILD_ROOT}%{libdir}
    %{__cp} -a webapps/* ${RPM_BUILD_ROOT}%{appdir}
popd

%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > ${RPM_BUILD_ROOT}%{confdir}/%{name}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE3} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE4} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{name}
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service
%{__install} -m 0644 %{SOURCE20} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}-jsvc.service
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE7} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE21} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE30} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE31} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server
%{__install} -m 0644 %{SOURCE32} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service

# Substitute libnames in catalina-tasks.xml
sed -i \
   "s,el-api.jar,%{name}-el-%{elspec}-api.jar,;
    s,servlet-api.jar,%{name}-servlet-%{servletspec}-api.jar,;
    s,jsp-api.jar,%{name}-jsp-%{jspspec}-api.jar,;" \
    ${RPM_BUILD_ROOT}%{bindir}/catalina-tasks.xml

# create jsp and servlet API symlinks
pushd ${RPM_BUILD_ROOT}%{_javadir}
   %{__mv} %{name}/jsp-api.jar %{name}-jsp-%{jspspec}-api.jar
   %{__ln_s} %{name}-jsp-%{jspspec}-api.jar %{name}-jsp-api.jar
   %{__mv} %{name}/servlet-api.jar %{name}-servlet-%{servletspec}-api.jar
   %{__ln_s} %{name}-servlet-%{servletspec}-api.jar %{name}-servlet-api.jar
   %{__mv} %{name}/el-api.jar %{name}-el-%{elspec}-api.jar
   %{__ln_s} %{name}-el-%{elspec}-api.jar %{name}-el-api.jar
popd

pushd output/build
    %{_bindir}/build-jar-repository lib ecj 2>&1
    # need to use -p here with b-j-r otherwise the examples webapp fails to
    # load with a java.io.IOException
    %{_bindir}/build-jar-repository -p webapps/examples/WEB-INF/lib \
    tomcat-taglibs-standard/taglibs-standard-impl.jar tomcat-taglibs-standard/taglibs-standard-compat.jar 2>&1
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/%{name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/%{name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/%{name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath ecj/ecj) jasper-jdt.jar

    # Temporary copy the juli jar here from /usr/share/java/tomcat (for maven depmap)
    %{__cp} -a ${RPM_BUILD_ROOT}%{bindir}/tomcat-juli.jar ./
popd

# symlink to the FHS locations where we've installed things
pushd ${RPM_BUILD_ROOT}%{homedir}
    %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{libdir} lib
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

# install sample webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/sample
pushd ${RPM_BUILD_ROOT}%{appdir}/sample
%{jar} xf ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war
popd
%{__rm} ${RPM_BUILD_ROOT}%{appdir}/docs/appdev/sample/sample.war

# Allow linking for example webapp
%{__mkdir_p} ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
pushd ${RPM_BUILD_ROOT}%{appdir}/examples/META-INF
echo '<?xml version="1.0" encoding="UTF-8"?>' > context.xml
echo '<Context>' >> context.xml
echo '  <Resources allowLinking="true" />' >> context.xml
echo '</Context>' >> context.xml
popd

pushd ${RPM_BUILD_ROOT}%{appdir}/examples/WEB-INF/lib
%{__ln_s} -f $(build-classpath tomcat-taglibs-standard/taglibs-standard-impl) jstl.jar
%{__ln_s} -f $(build-classpath tomcat-taglibs-standard/taglibs-standard-compat) standard.jar
popd


# Install the maven metadata
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_mavenpomdir}
pushd output/dist/src/res/maven
for pom in *.pom; do
    # fix-up version in all pom files
    sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
done

# we won't install dbcp, juli-adapters and juli-extras pom files
for libname in annotations-api catalina jasper-el jasper catalina-ha; do
    %{__cp} -a %{name}-$libname.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-$libname.pom
    %add_maven_depmap JPP.%{name}-$libname.pom %{name}/$libname.jar -f "tomcat-lib"
done

# tomcat-util-scan
%{__cp} -a %{name}-util-scan.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-util-scan.pom
%add_maven_depmap JPP.%{name}-util-scan.pom %{name}/%{name}-util-scan.jar -f "tomcat-lib"

# tomcat-jni
%{__cp} -a %{name}-jni.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-jni.pom
%add_maven_depmap JPP.%{name}-jni.pom %{name}/%{name}-jni.jar -f "tomcat-lib"

# servlet-api jsp-api and el-api are not in tomcat subdir, since they are widely re-used elsewhere
%{__cp} -a tomcat-jsp-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-jsp-api.pom
%add_maven_depmap JPP-tomcat-jsp-api.pom tomcat-jsp-api.jar -f "tomcat-jsp-api" -a "org.eclipse.jetty.orbit:javax.servlet.jsp"

%{__cp} -a tomcat-el-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-el-api.pom
%add_maven_depmap JPP-tomcat-el-api.pom tomcat-el-api.jar -f "tomcat-el-api" -a "org.eclipse.jetty.orbit:javax.el"

%{__cp} -a tomcat-servlet-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP-tomcat-servlet-api.pom
# Generate a depmap fragment javax.servlet:servlet-api pointing to
# tomcat-servlet-3.0-api for backwards compatibility
# also provide jetty depmap (originally in jetty package, but it's cleaner to have it here
%add_maven_depmap JPP-tomcat-servlet-api.pom tomcat-servlet-api.jar -f "tomcat-servlet-api"

# replace temporary copy with link
%{__ln_s} -f $(abs2rel %{bindir}/tomcat-juli.jar %{libdir}) ${RPM_BUILD_ROOT}%{libdir}/

# two special pom where jar files have different names
%{__cp} -a tomcat-tribes.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-catalina-tribes.pom
%add_maven_depmap JPP.%{name}-catalina-tribes.pom %{name}/catalina-tribes.jar

%{__cp} -a tomcat-coyote.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-coyote.pom
%add_maven_depmap JPP.%{name}-tomcat-coyote.pom %{name}/tomcat-coyote.jar

%{__cp} -a tomcat-juli.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-juli.pom
%add_maven_depmap JPP.%{name}-tomcat-juli.pom %{name}/tomcat-juli.jar

%{__cp} -a tomcat-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-api.pom
%add_maven_depmap JPP.%{name}-tomcat-api.pom %{name}/tomcat-api.jar

%{__cp} -a tomcat-util.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-util.pom
%add_maven_depmap JPP.%{name}-tomcat-util.pom %{name}/tomcat-util.jar

%{__cp} -a tomcat-jdbc.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-jdbc.pom
%add_maven_depmap JPP.%{name}-tomcat-jdbc.pom %{name}/tomcat-jdbc.jar

# tomcat-websocket-api
%{__cp} -a tomcat-websocket-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-websocket-api.pom
%add_maven_depmap JPP.%{name}-websocket-api.pom %{name}/websocket-api.jar

# tomcat-tomcat-websocket
%{__cp} -a tomcat-websocket.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-tomcat-websocket.pom
%add_maven_depmap JPP.%{name}-tomcat-websocket.pom %{name}/tomcat-websocket.jar

# tomcat-jaspic-api
%{__cp} -a tomcat-jaspic-api.pom ${RPM_BUILD_ROOT}%{_mavenpomdir}/JPP.%{name}-jaspic-api.pom
%add_maven_depmap JPP.%{name}-jaspic-api.pom %{name}/jaspic-api.jar


%pre
# add the tomcat user and group
getent group tomcat >/dev/null || %{_sbindir}/groupadd -f -g %{tcuid} -r tomcat
if ! getent passwd tomcat >/dev/null ; then
    if ! getent passwd %{tcuid} >/dev/null ; then
        %{_sbindir}/useradd -r -u %{tcuid} -g tomcat -d %{homedir} -s /usr/sbin/nologin -c "Apache Tomcat" tomcat
        # Tomcat uses a reserved ID, so there should never be an else
    fi
fi
exit 0

%post
# install but don't activate
%systemd_post %{name}.service

%post jsp-%{jspspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/jsp.jar jsp \
    %{_javadir}/%{name}-jsp-%{jspspec}-api.jar 20200

%post servlet-%{servletspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/servlet.jar servlet \
    %{_javadir}/%{name}-servlet-%{servletspec}-api.jar 30000

%post el-%{elspec}-api
%{_sbindir}/update-alternatives --install %{_javadir}/elspec.jar elspec \
   %{_javadir}/%{name}-el-%{elspec}-api.jar 20300

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service 

%postun jsp-%{jspspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jsp \
        %{_javadir}/%{name}-jsp-%{jspspec}-api.jar
fi

%postun servlet-%{servletspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove servlet \
        %{_javadir}/%{name}-servlet-%{servletspec}-api.jar
fi

%postun el-%{elspec}-api
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove elspec \
        %{_javadir}/%{name}-el-%{elspec}-api.jar
fi

%files 
%defattr(0664,root,tomcat,0755)
%license LICENSE
%doc {NOTICE,RELEASE*}
%attr(0755,root,root) %{_bindir}/%{name}-digest
%attr(0755,root,root) %{_bindir}/%{name}-tool-wrapper
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %{_unitdir}/%{name}@.service
%attr(0755,root,root) %dir %{_libexecdir}/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/%{name}/functions
%attr(0755,root,root) %{_libexecdir}/%{name}/preamble
%attr(0755,root,root) %{_libexecdir}/%{name}/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}

%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}

%defattr(0664,root,tomcat,0770)
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}

%defattr(0644,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0755,root,tomcat) %dir %{confdir}/conf.d
%{confdir}/conf.d/README
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/context.xml
%config(noreplace) %{confdir}/server.xml
%attr(0640,root,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%attr(0664,root,tomcat) %{confdir}/tomcat-users.xsd
%attr(0664,root,tomcat) %config(noreplace) %{confdir}/jaspic-providers.xml
%attr(0664,root,tomcat) %{confdir}/jaspic-providers.xsd
%config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{bindir}/bootstrap.jar
%{bindir}/catalina-tasks.xml
%{homedir}/lib
%{homedir}/temp
%{homedir}/webapps
%{homedir}/work
%{homedir}/logs
%{homedir}/conf

%files admin-webapps
%defattr(0664,root,tomcat,0755)
%{appdir}/host-manager
%{appdir}/manager

%files docs-webapp
%{appdir}/docs

%files jsp-%{jspspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-jsp-api
%{_javadir}/%{name}-jsp-%{jspspec}*.jar

%files lib -f output/dist/src/res/maven/.mfiles-tomcat-lib
%dir %{libdir}
%{libdir}/*.jar
%{_javadir}/*.jar
%{bindir}/tomcat-juli.jar
%{_mavenpomdir}/JPP.%{name}-annotations-api.pom
%{_mavenpomdir}/JPP.%{name}-catalina-ha.pom
%{_mavenpomdir}/JPP.%{name}-catalina-tribes.pom
%{_mavenpomdir}/JPP.%{name}-catalina.pom
%{_mavenpomdir}/JPP.%{name}-jasper-el.pom
%{_mavenpomdir}/JPP.%{name}-jasper.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-api.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-juli.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-coyote.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-util.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-jdbc.pom
%{_mavenpomdir}/JPP.%{name}-websocket-api.pom
%{_mavenpomdir}/JPP.%{name}-tomcat-websocket.pom
%{_mavenpomdir}/JPP.%{name}-jaspic-api.pom
%{_datadir}/maven-metadata/tomcat.xml
%exclude %{libdir}/%{name}-el-%{elspec}-api.jar
%exclude %{_javadir}/%{name}-servlet-%{servletspec}*.jar
%exclude %{_javadir}/%{name}-el-%{elspec}-api.jar
%exclude %{_javadir}/%{name}-jsp-%{jspspec}*.jar

%files servlet-%{servletspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-servlet-api
%license LICENSE
%{_javadir}/%{name}-servlet-%{servletspec}*.jar

%files el-%{elspec}-api -f output/dist/src/res/maven/.mfiles-tomcat-el-api
%license LICENSE
%{_javadir}/%{name}-el-%{elspec}-api.jar
%{libdir}/%{name}-el-%{elspec}-api.jar

%files webapps
%defattr(0644,tomcat,tomcat,0755)
%{appdir}/ROOT
%{appdir}/examples
%{appdir}/sample

%files jsvc
%defattr(755,root,root,0755)
%attr(0644,root,root) %{_unitdir}/%{name}-jsvc.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0660,tomcat,tomcat) %verify(not size md5 mtime) %{logdir}/catalina.out

%changelog
* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 9.0.39-6
- Rename java-headless dependency to java
- Change Source URL to pull from Apache arhive
- License verified

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 9.0.39-5
- Remove epoch

* Fri Aug 13 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:9.0.39-4
- Removed epoch from required packages where Mariner doesn't include the epoch number.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:9.0.39-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Fri Dec 18 2020 Hui Wang <huwang@redhat.com> - 1:9.0.39-2
- Related: rhbz#64830 concurrency issue in HPACK decoder (CVE-2020-17527)

* Mon Oct 12 2020 Hui Wang <huwang@redhat.com> - 1:9.0.39-1
- Update to 9.0.39
- Revert upstream fix d1f4d8712ddb52857f40a8cc4a82bf8b8e013f88 for LogFactory.java because of our lower version of bnd 

* Mon Sep 21 2020 Hui Wang <huwang@redhat.com> - 1:9.0.38-2
- Related: rhbz#1857043 Temporarily remove OSGi metadata from tomcat jars

* Wed Sep 16 2020 Hui Wang <huwang@redhat.com> - 1:9.0.38-1
- Update to 9.0.38

* Wed Jul 15 2020 Hui Wang <huwang@redhat.com> - 1:9.0.37-1
- Upgrade to 9.0.37

* Wed Jun 10 2020 Hui Wang <huwang@redhat.com> - 1:9.0.36-1
- Upgrade to 9.0.36

* Sun May 31 2020 Hui Wang <huwang@redhat.com> - 1:9.0.35-2
- Upgrade to 9.0.35

* Wed Apr 22 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.34-2
- Add updated catalina.policy patch to allow ECJ usage under the Security Manager

* Tue Apr 21 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.34-1
- Update to 9.0.34

* Thu Mar 12 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.31-2
- Related: rhbz#1806398 Undo changes in defaults for AJP connector (CVE-2020-1938) to prevent breakage, please update your configuration accordingly

* Thu Mar 05 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.31-1
- Update to 9.0.31
- Resolves: rhbz#1806398 - CVE-2020-1938 tomcat: Apache Tomcat AJP File Read/Inclusion Vulnerability

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.30-1
- Update to 9.0.30

* Thu Sep 26 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.26-2
- Resolves: rhbz#1510522 man page uid and gid mismatch for service accounts

* Thu Sep 26 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.26-1
- Update to 9.0.26
- Resolves: rhbz#1523112 tomcat systemd does not cope with - in service names
- Resolves: rhbz#1510896 Problem to start tomcat with a user whose group has a name different to the user

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.21-2
- Update build-classpath calls to ECJ to specify the JAR we want to use

* Tue Jun 18 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.21-1
- Update to 9.0.21

* Tue Apr 02 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.13-4
- Remove javadoc subpackage to drop the jpackage-utils dependency

* Wed Feb 20 2019 Coty Sutherland <csutherl@redhat.com> - 1:9.0.13-3
- Remove OSGi MANIFEST files, these are now included in the upstream Tomcat distribution (as of 9.0.10)
- Remove unused dependencies, apache-commons-collections, apache-commons-daemon, apache-commons-pool, junit

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Coty Sutherland <csutherl@redhat.com> - 1:9.0.13-1
- Update to 9.0.13
- Resolves: rhbz#1636513 - CVE-2018-11784 tomcat: Open redirect in default servlet

* Sun Oct 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1:9.0.10-2
- Drop legcy sys-v bits

* Tue Jul 31 2018 Coty Sutherland <csutherl@redhat.com> - 1:9.0.10-1
- Update to 9.0.10
- Resolves: rhbz#1624929 - CVE-2018-1336 tomcat: A bug in the UTF-8 decoder can lead to DoS
- Resolves: rhbz#1579612 - CVE-2018-8014 tomcat: Insecure defaults in CORS filter enable 'supportsCredentials' for all origins
- Resolves: rhbz#1607586 - CVE-2018-8034 tomcat: host name verification missing in WebSocket client
- Resolves: rhbz#1607584 - CVE-2018-8037 tomcat: Due to a mishandling of close in NIO/NIO2 connectors user sessions can get mixed up

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 01 2018 Coty Sutherland <csutherl@redhat.com> - 1:9.0.7-1
- Update to 9.0.7

* Thu Mar 15 2018 Coty Sutherland <csutherl@redhat.com> - 1:8.5.29-1
- Update to 8.5.29
- Resolves: rhbz#1548290 CVE-2018-1304 tomcat: Incorrect handling of empty string URL in security constraints can lead to unitended exposure of resources
- Resolves: rhbz#1548284 CVE-2018-1305 tomcat: Late application of security constraints can lead to resource exposure for unauthorised users

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:8.0.49-2
- Escape macros in %%changelog

* Thu Feb 01 2018 Coty Sutherland <csutherl@redhat.com> - 1:8.0.49-1
- Update to 8.0.49

* Tue Dec 12 2017 Merlin Mathesius <mmathesi@redhat.com> - 1:8.0.47-3
- Cleanup spec file conditionals

* Tue Oct 24 2017 Troy Dawson <tdawson@redhat.com> - 1:8.0.47-2
- Change "zip -u" to "zip"
- Resolves: rhbz#1495241 [tomcat] zip -u in spec file causes race condition

* Wed Oct 04 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.47-1
- Update to 8.0.47
- Resolves: rhbz#1497682 CVE-2017-12617 tomcat: Remote Code Execution bypass for CVE-2017-12615

* Mon Aug 21 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.46-1
- Update to 8.0.46
- Resolves: rhbz#1480620 CVE-2017-7674 tomcat: Cache Poisoning

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 09 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.44-1
- Resolves: rhbz#1459160 CVE-2017-5664 tomcat: Security constrained bypass in error page mechanism

* Tue Apr 11 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.43-1
- Update to 8.0.43

* Fri Mar 31 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.42-1
- Update to 8.0.42

* Thu Feb 16 2017 Coty Sutherland <csutherl@redhat.com> - 1:8.0.41-1
- Update to 8.0.41
- Resolves: rhbz#1403825 CVE-2016-8745 tomcat: information disclosure due to incorrect Processor sharing

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.39-1
- Update to 8.0.39
- Resolves: rhbz#1397493 CVE-2016-6816 CVE-2016-6817 CVE-2016-8735 tomcat: various flaws

* Tue Oct 25 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.38-1
- Update to 8.0.38

* Sun Oct 23 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.37-3
- Resolves: rhbz#1383216 CVE-2016-6325 tomcat: tomcat writable config files allow privilege escalation
- Resolves: rhbz#1382310 CVE-2016-5425 tomcat: Local privilege escalation via systemd-tmpfiles service

* Tue Sep 13 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.37-1
- Rebase to 8.0.37
- Resolves: rhbz#1375581 CVE-2016-5388 CGI sets environmental variable based on user supplied Proxy request header
- Resolves: rhbz#1370262 catalina.out is no longer in use in the main package, but still gets rotated

* Thu Aug 11 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.36-2
- Related: rhbz#1349469 Correct typo in changelog entry

* Mon Aug 08 2016 Coty Sutherland <csutherl@redhat.com> - 1:8.0.36-1
- Resolves: rhbz#1349469 CVE-2016-3092 tomcat: Usage of vulnerable FileUpload package can result in denial of service (updates to 8.0.36)
- Resolves: rhbz#1364056 The command tomcat-digest doesn't work
- Resolves: rhbz#1363884 The tomcat-tool-wrapper script is broken
- Resolves: rhbz#1347864 The systemd service unit does not allow tomcat to shut down gracefully
- Resolves: rhbz#1347835 The security manager doesn't work correctly (JSPs cannot be compiled)
- Resolves: rhbz#1341853 rpm -V tomcat fails on /var/log/tomcat/catalina.out
- Resolves: rhbz#1341850 tomcat-jsvc.service has TOMCAT_USER value hard-coded
- Resolves: rhbz#1359737 Missing maven depmap for the following artifacts: org.apache.tomcat:tomcat-websocket, org.apache.tomcat:tomcat-websocket-api
- Resolves: asfbz#59960  Building javadocs with java8 fails

* Wed Mar 2 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-4
- Revert sysconfig migration changes, resolves: rhbz#1311771, rhbz#1311905
- Add /etc/tomcat/conf.d/ with shell expansion support, resolves rhbz#1293636

* Sat Feb 27 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-3
- Load sysconfig from tomcat.conf, resolves: rhbz#1311771, rhbz#1311905
- Set default javax.sql.DataSource factory to apache commons one, resolves rhbz#1214381

* Sun Feb 21 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-2
- Fix symlinks from $CATALINA_HOME/lib perspective, resolves: rhbz#1308685

* Thu Feb 11 2016 Ivan Afonichev <ivan.afonichev@gmail.com> - 1:8.0.32-1
- Updated to 8.0.32
- Remove log4j support. It has never been working actually. See rhbz#1236297
- Move shipped config to /etc/sysconfig/tomcat. /etc/tomcat/tomcat.conf can now be used to override it with shell expansion, resolves rhbz#1293636
- Recommend tomcat-native, resolves: rhbz#1243132

* Wed Feb 10 2016 Coty Sutherland <csutherl@redhat.com> 1:8.0.26-4
- Resolves: rhbz#1286800 Failed to start component due to wrong allowLinking="true" in context.xml
- Program /bin/nologin does not exist (#1302718)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Robert Scheck <robert@fedoraproject.org> 1:8.0.26-2
- CATALINA_OPTS are only read when SECURITY_MANAGER is true (#1147105)

* Thu Aug 27 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.26-1
- Update to 8.0.26.

* Fri Jul 10 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.24-2
- Update to 8.0.24.

* Fri Jun 19 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.23-2
- Drop javax.el:el-api alias.

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.23-1
- Update to 8.0.23.

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.20-3
- Drop jetty alias for servlet.

* Tue Jun 09 2015 Michal Srb <msrb@redhat.com> - 1:8.0.20-2
- Fix metadata for org.apache.tomcat:{tomcat-jni,tomcat-util-scan}

* Thu Mar 5 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.18-5
- Rebuild against tomcat-taglibs-standard.

* Wed Mar 4 2015 Alexander Kurtakov <akurtako@redhat.com> 1:8.0.18-4
- Fix epoch bumped el_1_0_api that would override all other glassfish/jboss/etc. due to wrong epoch.
- Drop old provides. 

* Tue Mar 03 2015 Stephen Gallagher <sgallagh@redhat.com> 1:8.0.18-3
- Bump epoch to maintain upgrade path from Fedora 22

* Mon Feb 16 2015 Michal Srb <msrb@redhat.com> - 0:8.0.18-2
- Install POM files for org.apache.tomcat:{tomcat-jni,tomcat-util-scan}

* Sun Feb 15 2015 Ivan Afonichev <ivan.afonichev@gmail.com> 0:8.0.18-1
- Updated to 8.0.18

* Sat Sep 20 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:8.0.12-1
- Updated to 8.0.12
- Substitute libnames in catalina-tasks.xml, resolves: rhbz#1126439
- Use CATALINA_OPTS only on start, resolves: rhbz#1051194

* Mon Jun 16 2014 Michal Srb <msrb@redhat.com> - 0:7.0.54-3
- jsp-api requires el-api

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.54-1
- Update to upstream 7.0.54 - fixes compile with Java 8.

* Wed May 21 2014 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.52-3
- Drop servlet/el api provides to reduce user machines ending with both.

* Sun Mar 30 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.52-2
- Don't provide maven javax.jsp:jsp-api and javax.servlet.jsp:javax.servlet.jsp-api resolves: rhbz#1076949
- Move log4j support into subpackage, resolves: rhbz#1027716

* Wed Mar 26 2014 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.52-1
- Updated to 7.0.52
- Rewrite jsvc implementation, resolves: rhbz#1051743
- Switch to java-headless R, resolves: rhbz#1068566
- Create and own %%{_localstatedir}/lib/tomcats, resolves: rhbz#1026741
- Add pom for tomcat-jdbc, resolves: rhbz#1011003 

* Tue Jan 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.47-3
- Fix installation of Maven metadata for tomcat-juli.jar
- Resolves: rhbz#1033664

* Wed Jan 15 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:7.0.47-2
- Rebuild for bug #1033664

* Sun Nov 03 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.47-1
- Updated to 7.0.47
- Fix java.security.policy

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.42-2
- Remove jpackage-utils R

* Thu Jul 11 2013 Dmitry Tikhonov <squall.sama@gmail.com> 0:7.0.42-1
- Updated to 7.0.42

* Tue Jun 11 2013 Paul Komkoff <i@stingr.net> 0:7.0.40-3
- Dropped systemv inits. Bye-bye.
- Updated the systemd wrappers to allow running multiple instances.
  Added wrapper scripts to do that, ported the original non-named
  service file to work with the same wrappers, updated
  /usr/sbin/tomcat to call systemctl.

* Sat May 11 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.40-1
- Updated to 7.0.40
- Resolves: rhbz 956569 added missing commons-pool link
- Remove ant-nodeps BR

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.37-2
- Add depmaps for org.eclipse.jetty.orbit
- Resolves: rhbz#917626

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.39-1
- Updated to 7.0.39

* Wed Feb 20 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.37-1
- Updated to 7.0.37

* Mon Feb 4 2013 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.35-1
- Updated to 7.0.35
- systemd SuccessExitStatus=143 for proper stop exit code processing

* Mon Dec 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.34-1
- Updated to 7.0.34
- ecj >= 4.2.1 now required
- Resolves: rhbz 889395 concat classpath correctly; chdir to $CATALINA_HOME

* Fri Dec 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-2
- Resolves: rhbz 883806 refix logdir ownership 

* Sun Dec 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.33-1
- Updated to 7.0.33
- Resolves: rhbz 873620 need chkconfig for update-alternatives

* Wed Oct 17 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.32-1
- Updated to 7.0.32
- Resolves: rhbz 842620 symlinks to taglibs

* Fri Aug 24 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.29-1
- Updated to 7.0.29
- Add pidfile as tmpfile
- Use systemd for running as unprivileged user
- Resolves: rhbz 847751 upgrade path was broken
- Resolves: rhbz 850343 use new systemd-rpm macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:7.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 2 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.28-1
- Updated to 7.0.28
- Resolves: rhbz 820119 Remove bundled apache-commons-dbcp
- Resolves: rhbz 814900 Added tomcat-coyote POM
- Resolves: rhbz 810775 Remove systemv stuff from %%post scriptlet
- Remove redhat-lsb R 

* Mon Apr 9 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-2
- Fixed native download hack

* Sat Apr 7 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.27-1
- Updated to 7.0.27
- Fixed jakarta-taglibs-standard BR and R

* Wed Mar 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:7.0.26-2
- Add more depmaps to J2EE apis to help jetty/glassfish updates

* Wed Mar 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 0:7.0.26-2
- Added the POM files for tomcat-api and tomcat-util (#803495)

* Wed Feb 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.26-1
- Updated to 7.0.26
- Bug 790334: Change ownership of logdir for logrotate

* Thu Feb 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-4
- Bug 790694: Priorities of jsp, servlet and el packages updated.

* Wed Feb 8 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.25-3
- Dropped indirect dependecy to tomcat 5

* Sun Jan 22 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-2
- Added hack for maven depmap of tomcat-juli absolute link [ -f ] pass correctly

* Sat Jan 21 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.25-1
- Updated to 7.0.25
- Removed EntityResolver patch (changes already in upstream sources)
- Place poms and depmaps in the same package as jars
- Added javax.servlet.descriptor to export-package of servlet-api
- Move several chkconfig actions and reqs to systemv subpackage
- New maven depmaps generation method
- Add patch to support java7. (patch sent upstream).
- Require java >= 1:1.6.0

* Fri Jan 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:7.0.23-5
- Exported javax.servlet.* packages in version 3.0 as 2.6 to make
  servlet-api compatible with Eclipse.

* Thu Jan 12 2012 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-4
- Move jsvc support to subpackage

* Wed Jan 11 2012 Alexander Kurtakov <akurtako@redhat.com> 0:7.0.23-2
- Add EntityResolver setter patch to jasper for jetty's need. (patch sent upstream).

* Mon Dec 12 2011 Joseph D. Wagner <joe@josephdwagner.info> 0:7.0.23-3
- Added support to /usr/sbin/tomcat-sysd and /usr/sbin/tomcat for
  starting tomcat with jsvc, which allows tomcat to perform some
  privileged operations (e.g. bind to a port < 1024) and then switch
  identity to a non-privileged user. Must add USE_JSVC="true" to
  /etc/tomcat/tomcat.conf or /etc/sysconfig/tomcat.

* Mon Nov 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.23-1
- Updated to 7.0.23

* Fri Nov 11 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-2
- Move tomcat-juli.jar to lib package
- Drop %%update_maven_depmap as in tomcat6
- Provide native systemd unit file ported from tomcat6

* Thu Oct 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.22-1
- Updated to 7.0.22

* Mon Oct 03 2011 Rex Dieter <rdieter@fedoraproject.org> - 0:7.0.21-3.1
- rebuild (java), rel-eng#4932

* Mon Sep 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-3
- Fix basedir mode

* Tue Sep 20 2011 Roland Grunberg <rgrunber@redhat.com> 0:7.0.21-2
- Add manifests for el-api, jasper-el, jasper, tomcat, and tomcat-juli.

* Thu Sep 8 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.21-1
- Updated to 7.0.21

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-3
- Require java = 1:1.6.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-2
- Require java < 1.7.0

* Mon Aug 15 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.20-1
- Updated to 7.0.20

* Tue Jul 26 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.19-1
- Updated to 7.0.19

* Tue Jun 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.16-1
- Updated to 7.0.16

* Mon Jun 6 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-3
- Added initial systemd service
- Fix some paths

* Sat May 21 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-2
- Fixed http source link
- Securify some permissions
- Added licenses for el-api and servlet-api
- Added dependency on jpackage-utils for the javadoc subpackage

* Sat May 14 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.14-1
- Updated to 7.0.14

* Thu May 5 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-4
- Provided local paths for libs
- Fixed dependencies
- Fixed update temp/work cleanup

* Mon May 2 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-3
- Fixed package groups
- Fixed some permissions
- Fixed some links
- Removed old tomcat6 crap

* Thu Apr 28 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-2
- Package now named just tomcat instead of tomcat7
- Removed Provides:  %%{name}-log4j
- Switched to apache-commons-* names instead of jakarta-commons-* .
- Remove the old changelog
- BR/R java >= 1:1.6.0 , same for java-devel
- Removed old tomcat6 crap

* Wed Apr 27 2011 Ivan Afonichev <ivan.afonichev@gmail.com> 0:7.0.12-1
- Tomcat7
