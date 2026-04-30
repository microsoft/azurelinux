## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

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

%global jspspec 3.1
%global major_version 10
%global minor_version 1
%global micro_version 46
%global packdname apache-tomcat-%{version}-src
%global servletspec 6.0
%global elspec 5.0
%global tcuid 53
# Recommended version is specified in java/org/apache/catalina/core/AprLifecycleListener.java
%global native_version 2.0.8


# FHS 3.0 compliant tree structure - http://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html
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

Name:          tomcat
Epoch:         1
Version:       %{major_version}.%{minor_version}.%{micro_version}
Release:       %autorelease
Summary:       Apache Servlet/JSP Engine, RI for Servlet %{servletspec}/JSP %{jspspec} API

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:       Apache-2.0
URL:           http://tomcat.apache.org/
Source0:       http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/src/%{packdname}.tar.gz
Source1:       %{name}-%{major_version}.%{minor_version}.conf
Source2:       %{name}-%{major_version}.%{minor_version}.sysconfig
Source3:       %{name}-%{major_version}.%{minor_version}.wrapper
Source4:       %{name}-%{major_version}.%{minor_version}.logrotate
Source5:       %{name}-%{major_version}.%{minor_version}-digest.script
Source6:       %{name}-%{major_version}.%{minor_version}-tool-wrapper.script
Source7:       %{name}-%{major_version}.%{minor_version}.service
Source8:       %{name}-functions
Source9:       %{name}-preamble
Source10:      %{name}-server
Source11:      %{name}-named.service
Source12:      module-start-up-parameters.conf

Patch0:        %{name}-%{major_version}.%{minor_version}-bootstrap-MANIFEST.MF.patch
Patch1:        %{name}-%{major_version}.%{minor_version}-tomcat-users-webapp.patch
Patch2:        %{name}-build.patch
Patch3:        %{name}-%{major_version}.%{minor_version}-catalina-policy.patch
Patch4:        %{name}-%{major_version}.%{minor_version}-bnd-annotation.patch
Patch5:        %{name}-%{major_version}.%{minor_version}-JDTCompiler.patch
Patch6:        rhbz-1857043.patch

BuildArch:     noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires: ant-openjdk25  >= 1.10.2
BuildRequires: ecj >= 4.20
BuildRequires: findutils
BuildRequires: java-25-devel >= 17
BuildRequires: javapackages-local-openjdk25
BuildRequires: aqute-bnd
BuildRequires: aqute-bndlib
BuildRequires: systemd
BuildRequires: tomcat-jakartaee-migration

Requires:      (java-headless >= 11 or java-25 >= 11)
Requires:      javapackages-tools
Requires:      %{name}-lib = %{epoch}:%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:    tomcat-native >= %{native_version}
%endif
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

# added after log4j sub-package was removed
Provides:         %{name}-log4j = %{epoch}:%{version}-%{release}

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
Requires: %{name} = %{epoch}:%{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package jsp-%{jspspec}-api
Summary: Apache Tomcat JavaServer Pages v%{jspspec} API Implementation Classes
Provides: jsp = %{jspspec}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-jsp-2.3-api < 1:9.1
Provides:  %{name}-jsp-2.3-api = %{?epoch:%{epoch}:}%{version}-%{release}


%description jsp-%{jspspec}-api
Apache Tomcat JSP API Implementation Classes.

%package lib
Summary: Libraries needed to run the Tomcat Web container
Requires: %{name}-jsp-%{jspspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-servlet-%{servletspec}-api = %{epoch}:%{version}-%{release}
Requires: %{name}-el-%{elspec}-api = %{epoch}:%{version}-%{release}
Requires: ecj >= 4.20
Recommends: tomcat-jakartaee-migration
Requires(preun): coreutils

%description lib
Libraries needed to run the Tomcat Web container.

%package servlet-%{servletspec}-api
Summary: Apache Tomcat Java Servlet v%{servletspec} API Implementation Classes
Provides: servlet = %{servletspec}
Obsoletes: %{name}-servlet-4.0-api < 1:9.1
Provides:  %{name}-servlet-4.0-api = %{?epoch:%{epoch}:}%{version}-%{release}

%description servlet-%{servletspec}-api
Apache Tomcat Servlet API Implementation Classes.

%package el-%{elspec}-api
Summary: Apache Tomcat Expression Language v%{elspec} API Implementation Classes
Provides: el_api = %{elspec}
Obsoletes: %{name}-el-3.0-api < 1:9.1
Provides:  %{name}-el-3.0-api = %{?epoch:%{epoch}:}%{version}-%{release}

%description el-%{elspec}-api
Apache Tomcat EL API Implementation Classes.

%package webapps
Summary: The ROOT web application for Apache Tomcat
Requires: %{name} = %{epoch}:%{version}-%{release}

%description webapps
The ROOT web application for Apache Tomcat.

%prep
%setup -q -n %{packdname}
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%patch 0 -p0
%patch 1 -p0
%patch 2 -p0
%patch 3 -p0
%patch 4 -p0
%patch 5 -p0
%patch 6 -p0

# Remove webservices naming resources as it's generally unused
%{__rm} -rf java/org/apache/naming/factory/webservices

# Configure maven files
%mvn_package ":tomcat-el-api" tomcat-el-api
%mvn_alias "org.apache.tomcat:tomcat-el-api" "jakarta.servlet:jakarta.servlet-api"
%mvn_package ":tomcat-jsp-api" tomcat-jsp-api
%mvn_alias "org.apache.tomcat:tomcat-jsp-api" "jakarta.servlet:jakarta.servlet.jsp"
%mvn_package ":tomcat-servlet-api" tomcat-servlet-api

# Create a sysusers.d config file
cat >tomcat.sysusers.conf <<EOF
u tomcat %{tcuid} 'Apache Tomcat' %{homedir} -
EOF


%build
# we don't care about the tarballs and we're going to replace jars
# so just create a dummy file for later removal
touch HACK

# who needs a build.properties file anyway
%{ant} -Dbase.path="." \
  -Dbuild.compiler="modern" \
  -Dcommons-daemon.jar="HACK" \
  -Dcommons-daemon.native.src.tgz="HACK" \
  -Djdt.jar="$(build-classpath ecj/ecj)" \
  -Dtomcat-native.tar.gz="HACK" \
  -Dtomcat-native.home="." \
  -Dcommons-daemon.native.win.mgr.exe="HACK" \
  -Dnsis.exe="HACK" \
  -Djaxrpc-lib.jar="HACK" \
  -Dwsdl4j-lib.jar="HACK" \
  -Dbnd.jar="$(build-classpath aqute-bnd/biz.aQute.bnd)" \
  -Dbnd-annotation.jar="$(build-classpath aqute-bnd/biz.aQute.bnd.annotation)" \
  -Dversion="%{version}" \
  -Dversion.build="%{micro_version}" \
  -Dmigration-lib.jar="$(build-classpath tomcat-jakartaee-migration/jakartaee-migration.jar)" \
  deploy

# remove some jars that we'll replace with symlinks later
%{__rm} output/build/bin/commons-daemon.jar output/build/lib/ecj.jar output/build/lib/jakartaee-migration.jar
# Remove the example webapps per Apache Tomcat Security Considerations
# see https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html
%{__rm} -rf output/build/webapps/examples


%install
# build initial path structure
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_sbindir}
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
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE2} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0755 %{SOURCE3} \
    ${RPM_BUILD_ROOT}%{_sbindir}/%{name}
%{__install} -m 0644 %{SOURCE7} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}.service
%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE4} \
    > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}.disabled
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE5} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE6} \
    > ${RPM_BUILD_ROOT}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE8} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/functions
%{__install} -m 0755 %{SOURCE9} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/preamble
%{__install} -m 0755 %{SOURCE10} \
    ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}/server
%{__install} -m 0644 %{SOURCE11} \
    ${RPM_BUILD_ROOT}%{_unitdir}/%{name}@.service

%{__install} -m 0644 %{SOURCE12} ${RPM_BUILD_ROOT}%{confdir}/conf.d/

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
    %{_bindir}/build-jar-repository lib tomcat-jakartaee-migration 2>&1
popd

pushd ${RPM_BUILD_ROOT}%{libdir}
    # symlink JSP and servlet API jars
    %{__ln_s} ../../java/%{name}-jsp-%{jspspec}-api.jar .
    %{__ln_s} ../../java/%{name}-servlet-%{servletspec}-api.jar .
    %{__ln_s} ../../java/%{name}-el-%{elspec}-api.jar .
    %{__ln_s} $(build-classpath ecj/ecj) jasper-jdt.jar
    %{__ln_s} $(build-classpath tomcat-jakartaee-migration/jakartaee-migration) jakartaee-migration.jar
    
    cp ../../%{name}/bin/tomcat-juli.jar .
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

# Install the maven metadata for the spec impl artifacts as other projects use them
#%{__install} -d -m 0755 ${RPM_BUILD_ROOT}%{_mavenpomdir}
pushd res/maven
    for pom in *.pom; do
        # fix-up version in all pom files
        sed -i 's/@MAVEN.DEPLOY.VERSION@/%{version}/g' $pom
    done
popd

# Configure and install maven artifacts
%mvn_artifact res/maven/tomcat-el-api.pom output/build/lib/el-api.jar
%mvn_artifact res/maven/tomcat-jsp-api.pom output/build/lib/jsp-api.jar
%mvn_artifact res/maven/tomcat-servlet-api.pom output/build/lib/servlet-api.jar

%mvn_file org.apache.tomcat:tomcat-annotations-api tomcat/annotations-api
%mvn_artifact res/maven/tomcat-annotations-api.pom ${RPM_BUILD_ROOT}%{libdir}/annotations-api.jar
%mvn_artifact res/maven/tomcat-api.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-api.jar
%mvn_file org.apache.tomcat:tomcat-catalina-ant tomcat/catalina-ant
%mvn_artifact res/maven/tomcat-catalina-ant.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ant.jar
%mvn_file org.apache.tomcat:tomcat-catalina-ha tomcat/catalina-ha
%mvn_artifact res/maven/tomcat-catalina-ha.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ha.jar
%mvn_file org.apache.tomcat:tomcat-catalina tomcat/catalina
%mvn_artifact res/maven/tomcat-catalina.pom ${RPM_BUILD_ROOT}%{libdir}/catalina.jar
%mvn_artifact res/maven/tomcat-coyote.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-coyote.jar
%mvn_artifact res/maven/tomcat-dbcp.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-dbcp.jar
%mvn_artifact res/maven/tomcat-i18n-cs.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-cs.jar
%mvn_artifact res/maven/tomcat-i18n-de.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-de.jar
%mvn_artifact res/maven/tomcat-i18n-es.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-es.jar
%mvn_artifact res/maven/tomcat-i18n-fr.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-fr.jar
%mvn_artifact res/maven/tomcat-i18n-ja.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ja.jar
%mvn_artifact res/maven/tomcat-i18n-ko.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ko.jar
%mvn_artifact res/maven/tomcat-i18n-pt-BR.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-pt-BR.jar
%mvn_artifact res/maven/tomcat-i18n-ru.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-ru.jar
%mvn_artifact res/maven/tomcat-i18n-zh-CN.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-i18n-zh-CN.jar
%mvn_file org.apache.tomcat:tomcat-jasper-el tomcat/jasper-el
%mvn_artifact res/maven/tomcat-jasper-el.pom ${RPM_BUILD_ROOT}%{libdir}/jasper-el.jar
%mvn_file org.apache.tomcat:tomcat-jasper tomcat/jasper
%mvn_artifact res/maven/tomcat-jasper.pom ${RPM_BUILD_ROOT}%{libdir}/jasper.jar
%mvn_file org.apache.tomcat:tomcat-jaspic-api tomcat/jaspic-api
%mvn_artifact res/maven/tomcat-jaspic-api.pom ${RPM_BUILD_ROOT}%{libdir}/jaspic-api.jar
%mvn_artifact res/maven/tomcat-jdbc.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-jdbc.jar
%mvn_artifact res/maven/tomcat-jni.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-jni.jar
%mvn_artifact res/maven/tomcat-juli.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-juli.jar
%mvn_file org.apache.tomcat:tomcat-ssi tomcat/catalina-ssi
%mvn_artifact res/maven/tomcat-ssi.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-ssi.jar
%mvn_file org.apache.tomcat:tomcat-storeconfig tomcat/catalina-storeconfig
%mvn_artifact res/maven/tomcat-storeconfig.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-storeconfig.jar
%mvn_file org.apache.tomcat:tomcat-tribes tomcat/catalina-tribes
%mvn_artifact res/maven/tomcat-tribes.pom ${RPM_BUILD_ROOT}%{libdir}/catalina-tribes.jar
%mvn_artifact res/maven/tomcat-util-scan.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util-scan.jar
%mvn_artifact res/maven/tomcat-util.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-util.jar
%mvn_file org.apache.tomcat:tomcat-websocket-api tomcat/websocket-api
%mvn_artifact res/maven/tomcat-websocket-api.pom ${RPM_BUILD_ROOT}%{libdir}/websocket-api.jar
%mvn_artifact res/maven/tomcat-websocket.pom ${RPM_BUILD_ROOT}%{libdir}/tomcat-websocket.jar
%mvn_artifact res/maven/tomcat-websocket-client-api.pom ${RPM_BUILD_ROOT}%{libdir}/websocket-client-api.jar
%mvn_artifact res/maven/tomcat.pom

%mvn_install

install -m0644 -D tomcat.sysusers.conf %{buildroot}%{_sysusersdir}/tomcat.conf

%post
# install but don't activate
%systemd_post %{name}.service

%preun
# clean tempdir and workdir on removal or upgrade
%{__rm} -rf %{workdir}/* %{tempdir}/*
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files 
%defattr(0664,root,tomcat,0755)
%doc {LICENSE,NOTICE,RELEASE*}
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.disabled
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
%{confdir}/conf.d/module-start-up-parameters.conf
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
%{_sysusersdir}/tomcat.conf

%files admin-webapps
%defattr(0664,root,tomcat,0755)
%{appdir}/host-manager
%{appdir}/manager

%files docs-webapp
%{appdir}/docs

%files lib -f .mfiles
%dir %{libdir}
%{libdir}/*.jar
%{_javadir}/*.jar
%{bindir}/tomcat-juli.jar
%exclude %{libdir}/%{name}-el-%{elspec}-api.jar
%exclude %{libdir}/%{name}-servlet-%{servletspec}*.jar
%exclude %{libdir}/%{name}-jsp-%{jspspec}*.jar
%exclude %{_javadir}/%{name}-servlet-%{servletspec}*.jar
%exclude %{_javadir}/%{name}-el-%{elspec}-api.jar
%exclude %{_javadir}/%{name}-jsp-%{jspspec}*.jar
%exclude %{_javadir}/%{name}-servlet-api.jar
%exclude %{_javadir}/%{name}-el-api.jar
%exclude %{_javadir}/%{name}-jsp-api.jar
%exclude %{_jnidir}/*

%files jsp-%{jspspec}-api -f .mfiles-tomcat-jsp-api
%{_javadir}/%{name}-jsp-%{jspspec}*.jar
%{libdir}/%{name}-jsp-%{jspspec}*.jar
%{_javadir}/%{name}-jsp-api.jar

%files servlet-%{servletspec}-api -f .mfiles-tomcat-servlet-api
%doc LICENSE
%{_javadir}/%{name}-servlet-%{servletspec}*.jar
%{libdir}/%{name}-servlet-%{servletspec}*.jar
%{_javadir}/%{name}-servlet-api.jar

%files el-%{elspec}-api -f .mfiles-tomcat-el-api
%doc LICENSE
%{_javadir}/%{name}-el-%{elspec}-api.jar
%{libdir}/%{name}-el-%{elspec}-api.jar
%{_javadir}/%{name}-el-api.jar

%files webapps
%defattr(0644,tomcat,tomcat,0755)
%{appdir}/ROOT

%changelog
* Fri Sep 12 2025 Dimitris Soumis <dsoumis@redhat.com> - 1:10.1.46-1
- Update to version 10.1.46

* Tue Aug 19 2025 Dimitris Soumis <dsoumis@redhat.com> - 1:10.1.43-7
- Add virtual provides to resolve installability issues

* Thu Aug 14 2025 Dimitris Soumis <dsoumis@redhat.com> - 1:10.1.43-6
- Rebuilt for the side tag f43-build-side-116701

* Tue Jul 29 2025 Dimitris Soumis <dsoumis@redhat.com> - 1:10.1.43-5
- Rebuilt for the side tag f43-build-side-114811

* Fri Jan 10 2025 Dimitris Soumis <dsoumis@redhat.com> - 1:10.1.34-1
- Update to version 10.1.34

* Mon Dec 09 2024 Packit <hello@packit.dev> - 1:9.0.98-1
- Update to version 9.0.98
- Resolves: rhbz#2331168

* Mon Dec 02 2024 Dimitris Soumis <dsoumis@redhat.com> - 1:9.0.97-1
- Update to version 9.0.97
- Resolves: rhbz#2327090

* Tue Oct 08 2024 Packit <hello@packit.dev> - 1:9.0.96-1
- Update to version 9.0.96
- Resolves: rhbz#2317237

* Tue Sep 17 2024 Packit <hello@packit.dev> - 1:9.0.95-1
- Update to version 9.0.95
- Resolves: rhbz#2312858

* Tue Sep 10 2024 Packit <hello@packit.dev> - 1:9.0.94-1
- Update to version 9.0.94
- Resolves: rhbz#2311320

* Tue Aug 06 2024 Packit <hello@packit.dev> - 1:9.0.93-1
- Update to version 9.0.93
- Resolves: rhbz#2303026

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1:9.0.91-1
- convert license to SPDX

* Thu Jul 11 2024 Dimitris Soumis <dsoumis@redhat.com> - 1:9.0.91-1
- Update to 9.0.91

* Thu Jun 20 2024 Dimitris Soumis <dsoumis@redhat.com> - 1:9.0.90-1
- Update to 9.0.90

* Fri Jun 7 2024 Dimitris Soumis <dsoumis@redhat.com> - 1:9.0.89-1
- Update to 9.0.89 

* Thu Feb 29 2024 Adam Williamson <awilliam@redhat.com> - 1:9.0.83-4
- Accept java-21-headless as one of the alternatives for java

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:9.0.83-3
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Hui Wang <huwang@redhat.com> - 1:9.0.83-1
- Update to 9.0.83

* Mon Oct 16 2023 Hui Wang <huwang@redhat.com> - 1:9.0.82-1
- Update to 9.0.82
- Resolves: rhbz#2244333 Wrong dbcp class in tomcat 9

* Wed Sep 13 2023 Hui Wang <huwang@redhat.com> - 1:9.0.80-1
- Update to 9.0.80
- Fix java version

* Fri Aug 04 2023 Hui Wang <huwang@redhat.com> - 1:9.0.78-4
- Fix files permission

* Wed Jul 26 2023 Hui Wang <huwang@redhat.com> - 1:9.0.78-3
- Exclude jnidir in the lib subpackage

* Tue Jul 25 2023 Hui Wang <huwang@redhat.com> - 1:9.0.78-2
- Resolves: rhbz#2224318 There are duplicated jars in the tomcat lib subpackage

* Tue Jul 25 2023 Hui Wang <huwang@redhat.com> - 1:9.0.78-1
- Resolves: rhbz#2224318 There are duplicated jars in the tomcat lib-subpackage
- Update to 9.0.78

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Hui Wang <huwang@redhat.com> - 1:9.0.76-2
- Resolves: rhbz#2189672 Missing Tomcat POM files in Fedora Rawhide
- Remove JDTCompiler patch because ecj has been update
- Update to 9.0.76
- Resolves: rhbz#2188218 Link bin/tomcat-juli.jar to /usr/share/java
- Move tomcat-jsp-2.3-api.jar,tomcat-servlet-4.0-api.jar and tomcat-el-api.jar to the subpackages

* Thu Jun 08 2023 Hui Wang <huwang@redhat.com> - 1:9.0.75-1
- Update to 9.0.75

* Fri Mar 17 2023 Hui Wang <huwang@redhat.com> - 1:9.0.73-1
- Update to 9.0.73

* Sun Jan 29 2023 Hui Wang <huwang@redhat.com> - 1:9.0.71-1
- Update to 9.0.71
- Remove osgi-annotations patch
- Add bnd-annotation dependency which is in bndlib package 

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Hui Wang <huwang@redhat.com> - 1:9.0.70-1
- Update to 9.0.70

* Thu Nov 03 2022 Hui Wang <huwang@redhat.com> - 1:9.0.68-1
- Update to 9.0.68

* Thu Jul 21 2022 Hui Wang <huwang@redhat.com> - 1:9.0.65-1
- Update to 9.0.65

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1:9.0.64-2
- Rebuilt for Drop i686 JDKs

* Tue Jun 21 2022 Hui Wang <huwang@redhat.com> - 1:9.0.64-1
- Update to 9.0.64
- Add osgi-annotations dependency back

* Thu Mar 10 2022 Coty Sutherland <csutherl@redhat.com> - 1:9.0.59-3
- Related: rhbz#2061424 Adjust fix so that it uses the proper env var

* Tue Mar 08 2022 Coty Sutherland <csutherl@redhat.com> - 1:9.0.59-2
- Resolves: rhbz#2061424 Add Java 9 start-up parameters to allow reflection

* Wed Mar 02 2022 Sonia Xu <sonix@amazon.com> - 1:9.0.59-1
- Update to 9.0.59
- Resolves: rhbz#2047419 - CVE-2022-23181 tomcat: local privilege escalation vulnerability

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:9.0.56-3
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 09 2021 Hui Wang <huwang@redhat.com> - 1:9.0.56-1
- Update to 9.0.56

* Tue Oct 12 2021 Hui Wang <huwang@redhat.com> - 1:9.0.55-1
- Update to 9.0.55

* Tue Oct 12 2021 Hui Wang <huwang@redhat.com> - 1:9.0.54-1
- Update to 9.0.54

* Thu Sep 16 2021 Hui Wang <huwang@redhat.com> - 1:9.0.53-1
- Update to 9.0.53

* Wed Aug 18 2021 Hui Wang <huwang@redhat.com> - 1:9.0.52-1
- Update to 9.0.52

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 06 2021 Hui Wang <huwang@redhat.com> - 1:9.0.50-1
- Update to 9.0.50

* Sat Jun 05 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.45-4
- Add back logrotate config file per devel list request
- Add mvn virtual provides back for the servlet, el, and jsp spec impls

* Fri Jun 04 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.45-3
- Drop geronimo-jaxrpc, which provided the webservices naming factory resources that are generally unused

* Thu Jun 03 2021 Coty Sutherland <csutherl@redhat.com> - 1:9.0.45-2
- Remove examples webapps from subpackage
- Updates to javapackages-local removed %%add_maven_depmap which broke the build,
  so I removed the maven artifacts as they aren't very useful anyway
- Drop JSVC support as it's not very useful these days
- Drop geronimo-saaj as it's no longer required

* Thu Apr 22 2021 Hui Wang <huwang@redhat.com> - 1:9.0.45-1
- Update to 9.0.45

* Thu Mar 18 2021 Hui Wang <huwang@redhat.com> - 1:9.0.44-1
- Update to 9.0.44

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:9.0.43-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Feb 03 2021 Hui Wang <huwang@redhat.com> - 1:9.0.43-1
- Update to 9.0.43

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Hui Wang <huwang@redhat.com> - 1:9.0.41-1
- Update to 9.0.41

* Wed Nov 18 2020 Hui Wang <huwang@redhat.com> - 1:9.0.40-1
- Update to 9.0.40

* Mon Oct 12 2020 Hui Wang <huwang@redhat.com> - 1:9.0.39-1
- Update to 9.0.39

* Wed Sep 16 2020 Hui Wang <huwang@redhat.com> - 1:9.0.38-1
- Update to 9.0.38

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:9.0.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.37-3
- Related: rhbz#1857043 Temporarily remove OSGi metadata from tomcat jars

* Mon Jul 20 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.37-2
- Resolves: rhbz#1857043 Add patch to reinclude o.a.t.util.net.jsse and o.a.t.util.moduler.modules in tomcat-coyote.jar

* Mon Jul 13 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.37-1
- Update to 9.0.37

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1:9.0.36-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 10 2020 Hui Wang <huwang@redhat.com> - 1:9.0.36-1
- Upgrade to 9.0.36

* Sun May 31 2020 Hui Wang <huwang@redhat.com> - 1:9.0.35-2
- Upgrade to 9.0.35

* Wed Apr 22 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.34-2
- Add updated catalina.policy patch to allow ECJ usage under the Security Manager

* Tue Apr 21 2020 Coty Sutherland <csutherl@redhat.com> - 1:9.0.34-1
- Update to 9.0.34

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
