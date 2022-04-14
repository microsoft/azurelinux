Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright (c) 2000-2007, JPackage Project
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

%global jtuid       110
%global username    %{name}
%global confdir     %{_sysconfdir}/%{name}
%global logdir      %{_localstatedir}/log/%{name}
%global homedir     %{_datadir}/%{name}
%global jettycachedir %{_localstatedir}/cache/%{name}
%global tempdir     %{jettycachedir}/temp
%global rundir      %{_localstatedir}/run/%{name}
%global jettylibdir %{_localstatedir}/lib/%{name}
%global appdir      %{jettylibdir}/webapps


%global addver  .v20200723

# minimal version required to build eclipse and thermostat
# eclipse needs: util, server, http, continuation, io, security, servlet
# thermostat needs: server, jaas, webapp
# above modules need: jmx, xml
%bcond_without  jp_minimal

Name:           jetty
Version:        9.4.31
Release:        4%{?dist}
Summary:        Java Webserver and Servlet Container

# Jetty is dual licensed under both ASL 2.0 and EPL 1.0, see NOTICE.txt
License:        (ASL 2.0 or EPL-1.0) and BSD and CDDL and GPLv2 and MIT
URL:            http://www.eclipse.org/jetty/
Source0:        https://github.com/eclipse/%{name}.project/archive/%{name}-%{version}%{addver}.tar.gz
Source1:        jetty.sh
Source3:        jetty.logrotate
Source5:        %{name}.service
# MIT license text taken from Utf8Appendable.java
Source6:        LICENSE-MIT

Patch1:         0001-Distro-jetty.home.patch

BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-local
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)

%if %{without jp_minimal}
BuildRequires:  maven-local
BuildRequires:  mvn(com.github.jnr:jnr-unixsocket)
BuildRequires:  mvn(javax.annotation:javax.annotation-api)
BuildRequires:  mvn(javax.enterprise:cdi-api)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.servlet.jsp:javax.servlet.jsp-api)
BuildRequires:  mvn(javax.servlet:jstl)
BuildRequires:  mvn(javax.transaction:javax.transaction-api)
BuildRequires:  mvn(javax.websocket:javax.websocket-api)
BuildRequires:  mvn(javax.websocket:javax.websocket-client-api)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-war-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-tools-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-artifact-transfer)
BuildRequires:  mvn(org.apache.taglibs:taglibs-standard-impl)
BuildRequires:  mvn(org.apache.taglibs:taglibs-standard-spec)
BuildRequires:  mvn(org.apache.tomcat:tomcat-jasper)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:  mvn(org.eclipse.jetty.alpn:alpn-api)
BuildRequires:  mvn(org.eclipse.jetty.orbit:javax.mail.glassfish)
BuildRequires:  mvn(org.eclipse.jetty.orbit:javax.security.auth.message)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-assembly-descriptors)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-schemas)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-test-helper)
BuildRequires:  mvn(org.jboss.weld.servlet:weld-servlet-core)
BuildRequires:  mvn(org.mongodb:mongo-java-driver)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.slf4j:slf4j-api)

BuildRequires:  mvn(org.mortbay.jetty.alpn:alpn-boot)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-artifact-remote-resources)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-distribution-remote-resources)
BuildRequires:  mvn(org.eclipse.jetty.toolchain:jetty-test-policy)
#BuildRequires:  mvn(org.eclipse.jetty.toolchain.setuid:jetty-setuid-java)
BuildRequires:  maven-javadoc-plugin
BuildRequires:  glassfish-el
BuildRequires:  systemd
BuildRequires:  junit5

# duplicate providers, choose one
BuildRequires:  jboss-websocket-1.0-api
Requires:       jboss-websocket-1.0-api
%endif

BuildArch:      noarch

# jp_minimal doesn't have main package
%if %{without jp_minimal}
# Explicit requires for javapackages-tools since jetty.sh script
# uses /usr/share/java-utils/java-functions
Requires:       javapackages-tools
Requires:       %{name}-annotations = %{version}-%{release}
Requires:       %{name}-ant = %{version}-%{release}
Requires:       %{name}-client = %{version}-%{release}
Requires:       %{name}-continuation = %{version}-%{release}
Requires:       %{name}-deploy = %{version}-%{release}
Requires:       %{name}-fcgi-client = %{version}-%{release}
Requires:       %{name}-fcgi-server = %{version}-%{release}
Requires:       %{name}-http = %{version}-%{release}
Requires:       %{name}-http-spi = %{version}-%{release}
Requires:       %{name}-io = %{version}-%{release}
Requires:       %{name}-jaas = %{version}-%{release}
Requires:       %{name}-jaspi = %{version}-%{release}
Requires:       %{name}-jmx = %{version}-%{release}
Requires:       %{name}-jndi = %{version}-%{release}
Requires:       %{name}-jsp = %{version}-%{release}
Requires:       %{name}-jspc-maven-plugin = %{version}-%{release}
Requires:       %{name}-maven-plugin = %{version}-%{release}
Requires:       %{name}-plus = %{version}-%{release}
Requires:       %{name}-proxy = %{version}-%{release}
Requires:       %{name}-rewrite = %{version}-%{release}
Requires:       %{name}-security = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}
Requires:       %{name}-servlet = %{version}-%{release}
Requires:       %{name}-servlets = %{version}-%{release}
Requires:       %{name}-start = %{version}-%{release}
Requires:       %{name}-unixsocket = %{version}-%{release}
Requires:       %{name}-util = %{version}-%{release}
Requires:       %{name}-util-ajax = %{version}-%{release}
Requires:       %{name}-webapp = %{version}-%{release}
Requires:       %{name}-xml = %{version}-%{release}
Requires:       %{name}-cdi = %{version}-%{release}
Requires:       %{name}-websocket-api = %{version}-%{release}
Requires:       %{name}-websocket-client = %{version}-%{release}
Requires:       %{name}-websocket-common = %{version}-%{release}
Requires:       %{name}-websocket-server = %{version}-%{release}
Requires:       %{name}-websocket-servlet = %{version}-%{release}
Requires:       %{name}-javax-websocket-client-impl = %{version}-%{release}
Requires:       %{name}-javax-websocket-server-impl = %{version}-%{release}
Requires:       %{name}-nosql = %{version}-%{release}
Requires:       %{name}-quickstart = %{version}-%{release}
Requires:       %{name}-jstl = %{version}-%{release}
Requires:       %{name}-alpn-client = %{version}-%{release}
Requires:       %{name}-alpn-server = %{version}-%{release}
Requires:       %{name}-http2-client = %{version}-%{release}
Requires:       %{name}-http2-common = %{version}-%{release}
Requires:       %{name}-http2-hpack = %{version}-%{release}
Requires:       %{name}-http2-http-client-transport = %{version}-%{release}
Requires:       %{name}-http2-server = %{version}-%{release}

Requires(pre):    shadow-utils
%{?systemd_ordering}


Provides:       group(%username) = %jtuid
Provides:       user(%username)  = %jtuid
%endif

# Hazelcast in Fedora is too old for jetty to build against (Added in F29)
Obsoletes:      %{name}-hazelcast < 9.4.18-1
# Infinispan in Fedora is too old for jetty to build against (Added in F31)
Obsoletes:      %{name}-infinispan < 9.4.18-1
# Eclipse no longer available (Added in F31)
Obsoletes:      %{name}-osgi-alpn < 9.4.18-1
Obsoletes:      %{name}-osgi-boot < 9.4.18-1
Obsoletes:      %{name}-osgi-boot-jsp < 9.4.18-1
Obsoletes:      %{name}-osgi-boot-warurl < 9.4.18-1
# Spring framework removed from Fedora (Added in F32)
Obsoletes:      %{name}-spring < 9.4.24-1

%if %{with jp_minimal}
# Remove left-over packages that would have broken deps when built in minimal mode
Obsoletes:      %{name}-project < 9.4.20-1
Obsoletes:      %{name}-annotations < 9.4.20-1
Obsoletes:      %{name}-ant < 9.4.20-1
Obsoletes:      %{name}-cdi < 9.4.20-1
Obsoletes:      %{name}-deploy < 9.4.20-1
Obsoletes:      %{name}-fcgi-client < 9.4.20-1
Obsoletes:      %{name}-fcgi-server < 9.4.20-1
Obsoletes:      %{name}-http-spi < 9.4.20-1
Obsoletes:      %{name}-jaspi < 9.4.20-1
Obsoletes:      %{name}-jndi < 9.4.20-1
Obsoletes:      %{name}-jsp < 9.4.20-1
Obsoletes:      %{name}-jstl < 9.4.20-1
Obsoletes:      %{name}-jspc-maven-plugin < 9.4.20-1
Obsoletes:      %{name}-maven-plugin < 9.4.20-1
Obsoletes:      %{name}-plus < 9.4.20-1
Obsoletes:      %{name}-proxy < 9.4.20-1
Obsoletes:      %{name}-quickstart < 9.4.20-1
Obsoletes:      %{name}-rewrite < 9.4.20-1
Obsoletes:      %{name}-servlets < 9.4.20-1
Obsoletes:      %{name}-start < 9.4.20-1
Obsoletes:      %{name}-unixsocket < 9.4.20-1
Obsoletes:      %{name}-util-ajax < 9.4.20-1
Obsoletes:      %{name}-websocket-api < 9.4.20-1
Obsoletes:      %{name}-websocket-client < 9.4.20-1
Obsoletes:      %{name}-websocket-common < 9.4.20-1
Obsoletes:      %{name}-websocket-server < 9.4.20-1
Obsoletes:      %{name}-websocket-servlet < 9.4.20-1
Obsoletes:      %{name}-javax-websocket-client-impl < 9.4.20-1
Obsoletes:      %{name}-javax-websocket-server-impl < 9.4.20-1
Obsoletes:      %{name}-alpn-client < 9.4.20-1
Obsoletes:      %{name}-alpn-server < 9.4.20-1
Obsoletes:      %{name}-http2-client < 9.4.20-1
Obsoletes:      %{name}-http2-common < 9.4.20-1
Obsoletes:      %{name}-http2-hpack < 9.4.20-1
Obsoletes:      %{name}-http2-http-client-transport < 9.4.20-1
Obsoletes:      %{name}-http2-server < 9.4.20-1
Obsoletes:      %{name}-nosql < 9.4.20-1
%endif

%description
%global desc \
Jetty is a 100% Java HTTP Server and Servlet Container. This means that you\
do not need to configure and run a separate web server (like Apache) in order\
to use Java, servlets and JSPs to generate dynamic content. Jetty is a fully\
featured web server for static and dynamic content. Unlike separate\
server/container solutions, this means that your web server and web\
application run in the same process, without interconnection overheads\
and complications. Furthermore, as a pure java component, Jetty can be simply\
included in your application for demonstration, distribution or deployment.\
Jetty is available on all Java supported platforms.
%{desc}
%global extdesc %{desc}\
\
This package contains

# packages in jp_minimal set
%package        client
Summary:        client module for Jetty

%description    client
%{extdesc} %{summary}.

%package        continuation
Summary:        continuation module for Jetty

%description    continuation
%{extdesc} %{summary}.

%package        http
Summary:        http module for Jetty

%description    http
%{extdesc} %{summary}.

%package        http-spi
Summary:        http-spi module for Jetty

%description    http-spi
%{extdesc} %{summary}.

%package        io
Summary:        io module for Jetty

%description    io
%{extdesc} %{summary}.

%package        jaas
Summary:        jaas module for Jetty

%description    jaas
%{extdesc} %{summary}.

%package        jsp
Summary:        jsp module for Jetty
Requires:       glassfish-el

%description    jsp
%{extdesc} %{summary}.

%package        security
Summary:        security module for Jetty

%description    security
%{extdesc} %{summary}.

%package        server
Summary:        server module for Jetty

%description    server
%{extdesc} %{summary}.

%package        servlet
Summary:        servlet module for Jetty
# Eclipse no longer available (Added in F31)
Obsoletes:      %{name}-httpservice < 9.4.18-1

%description    servlet
%{extdesc} %{summary}.

%package        util
Summary:        util module for Jetty
# Utf8Appendable.java is additionally under MIT license
License:        (ASL 2.0 or EPL-1.0) and MIT

%description    util
%{extdesc} %{summary}.

%package        webapp
Summary:        webapp module for Jetty

%description    webapp
%{extdesc} %{summary}.

%package        jmx
Summary:        jmx module for Jetty

%description    jmx
%{extdesc} %{summary}.

%package        xml
Summary:        xml module for Jetty

%description    xml
%{extdesc} %{summary}.



%if %{without jp_minimal}
%package        project
Summary:        POM files for Jetty
Obsoletes:      %{name}-websocket-parent < 9.4.0-0.4
Provides:       %{name}-websocket-parent = %{version}-%{release}
Obsoletes:      %{name}-osgi-project < 9.4.0-0.4
Provides:       %{name}-osgi-project = %{version}-%{release}

%description    project
%{extdesc} %{summary}.

%package        deploy
Summary:        deploy module for Jetty

%description    deploy
%{extdesc} %{summary}.

%package        annotations
Summary:        annotations module for Jetty

%description    annotations
%{extdesc} %{summary}.

%package        ant
Summary:        ant module for Jetty

%description    ant
%{extdesc} %{summary}.

%package cdi
Summary:        Jetty CDI Configuration

%description cdi
%{extdesc} %{summary}.

%package        fcgi-client
Summary:        FastCGI client module for Jetty

%description    fcgi-client
%{extdesc} %{summary}.

%package        fcgi-server
Summary:        FastCGI client module for Jetty

%description    fcgi-server
%{extdesc} %{summary}.

%package        jaspi
Summary:        jaspi module for Jetty

%description    jaspi
%{extdesc} %{summary}.

%package        jndi
Summary:        jndi module for Jetty

%description    jndi
%{extdesc} %{summary}.

%package        jspc-maven-plugin
Summary:        jspc-maven-plugin module for Jetty

%description    jspc-maven-plugin
%{extdesc} %{summary}.

%package        maven-plugin
Summary:        maven-plugin module for Jetty

%description    maven-plugin
%{extdesc} %{summary}.

%package        plus
Summary:        plus module for Jetty

%description    plus
%{extdesc} %{summary}.

%package        proxy
Summary:        proxy module for Jetty

%description    proxy
%{extdesc} %{summary}.

%package        rewrite
Summary:        rewrite module for Jetty

%description    rewrite
%{extdesc} %{summary}.

%package        servlets
Summary:        servlets module for Jetty

%description    servlets
%{extdesc} %{summary}.

%package        start
Summary:        start module for Jetty

%description    start
%{extdesc} %{summary}.

%package        unixsocket
Summary:        unixsocket module for Jetty

%description    unixsocket
%{extdesc} %{summary}.

%package        util-ajax
Summary:        util-ajax module for Jetty

%description    util-ajax
%{extdesc} %{summary}.

%package        websocket-api
Summary:        websocket-api module for Jetty

%description    websocket-api
%{extdesc} %{summary}.

%package        websocket-client
Summary:        websocket-client module for Jetty

%description    websocket-client
%{extdesc} %{summary}.

%package        websocket-common
Summary:        websocket-common module for Jetty

%description    websocket-common
%{extdesc} %{summary}.

%package        websocket-server
Summary:        websocket-server module for Jetty

%description    websocket-server
%{extdesc} %{summary}.

%package        websocket-servlet
Summary:        websocket-servlet module for Jetty

%description    websocket-servlet
%{extdesc} %{summary}.

%package        javax-websocket-client-impl
Summary:        javax-websocket-client-impl module for Jetty

%description    javax-websocket-client-impl
%{extdesc} %{summary}.

%package        javax-websocket-server-impl
Summary:        javax-websocket-server-impl module for Jetty

%description    javax-websocket-server-impl
%{extdesc} %{summary}.

%package        nosql
Summary:        nosql module for Jetty

%description    nosql
%{extdesc} %{summary}.

%package        quickstart
Summary:        quickstart module for Jetty

%description    quickstart
%{extdesc} %{summary}.

%package        alpn-client
Summary:        alpn-client module for Jetty

%description    alpn-client
%{extdesc} %{summary}.

%package        alpn-server
Summary:        alpn-server module for Jetty

%description    alpn-server
%{extdesc} %{summary}.

%package        http2-client
Summary:        http2-client module for Jetty

%description    http2-client
%{extdesc} %{summary}.

%package        http2-common
Summary:        http2-common module for Jetty

%description    http2-common
%{extdesc} %{summary}.

%package        http2-hpack
Summary:        http2-hpack module for Jetty

%description    http2-hpack
%{extdesc} %{summary}.

%package        http2-http-client-transport
Summary:        http2-http-client-transport module for Jetty

%description    http2-http-client-transport
%{extdesc} %{summary}.

%package        http2-server
Summary:        http2-server module for Jetty

%description    http2-server
%{extdesc} %{summary}.

%package        jstl
Summary:        jstl module for Jetty

%description    jstl
%{extdesc} %{summary}.

%endif

%package        javadoc
Summary:        Javadoc for %{name}
# some MIT-licensed code (from Utf8Appendable) is used to generate javadoc
License:        (ASL 2.0 or EPL-1.0) and MIT

%description    javadoc
%{summary}.

%prep
%setup -q -n %{name}.project-%{name}-%{version}%{addver}

%patch1 -p1

find . -name "*.?ar" -exec rm {} \;
find . -name "*.class" -exec rm {} \;

# Plugins irrelevant or harmful to building the package
%pom_remove_plugin -r :maven-checkstyle-plugin
%pom_remove_plugin -r :findbugs-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :clirr-maven-plugin
%pom_remove_plugin -r :maven-eclipse-plugin
%pom_remove_plugin -r :maven-pmd-plugin
%pom_remove_plugin -r :license-maven-plugin
%pom_remove_plugin -r :maven-site-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-deploy-plugin
%pom_remove_plugin -r :jacoco-maven-plugin
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin -r :buildnumber-maven-plugin
%pom_remove_plugin -r :h2spec-maven-plugin

# Unnecessary pom flattening can be skipped
%pom_remove_plugin -r :flatten-maven-plugin jetty-bom

%pom_disable_module aggregates/jetty-all

# Reflective use of classes that might not be present in the JDK should be optional OSGi-wise
%pom_xpath_inject "pom:configuration/pom:instructions" \
"<Import-Package>sun.misc;resolution:=optional,com.sun.nio.file;resolution:=optional,*</Import-Package>"

# Use proper groupId for apache ant
%pom_xpath_replace "pom:groupId[text()='ant']" "<groupId>org.apache.ant</groupId>" jetty-ant/pom.xml

%pom_remove_dep "com.sun.net.httpserver:http" jetty-http-spi

%pom_change_dep -r org.mortbay.jasper:apache-jsp org.apache.tomcat:tomcat-jasper

%pom_add_dep 'org.junit.jupiter:junit-jupiter-engine:${junit.version}' tests/test-sessions/test-sessions-common

# provided by glassfish-jsp-api that has newer version
%pom_change_dep -r javax.servlet.jsp:jsp-api javax.servlet.jsp:javax.servlet.jsp-api

# txt artifact - not installable
%pom_remove_plugin ":jetty-version-maven-plugin"
%pom_xpath_remove "pom:artifactItem[pom:classifier='version']" jetty-home

# Disable building source release
%pom_xpath_remove 'pom:execution[pom:id="sources"]' jetty-home

# Unwanted JS in javadoc
sed -i '/^\s*\*.*<script>/d' jetty-util/src/main/java/org/eclipse/jetty/util/resource/Resource.java

# only used for integration tests
%pom_remove_plugin :maven-invoker-plugin jetty-jspc-maven-plugin

# These bundles have a dep on Eclipse that is not available on every arch
%pom_disable_module jetty-osgi

# We don't have asciidoctor-maven-plugin
%pom_disable_module jetty-documentation
%pom_remove_dep -r :jetty-documentation
%pom_xpath_remove 'pom:execution[pom:id="unpack-documentation"]' jetty-distribution

%pom_xpath_remove 'pom:artifactItem[pom:artifactId="libsetuid-osx"]' jetty-home/pom.xml

# TODO remove when jetty-setuid is packaged
%pom_xpath_remove "pom:execution[pom:id[text()='copy-setuid-deps']]" jetty-home/pom.xml

# We don't have gcloud-java-datastore in Fedora
%pom_disable_module jetty-gcloud
%pom_disable_module test-gcloud-sessions tests/test-sessions
%pom_remove_dep :jetty-gcloud-session-manager jetty-home

# we don't have com.googlecode.xmemcached:xmemcached yet
%pom_disable_module jetty-memcached
%pom_disable_module test-memcached-sessions tests/test-sessions
%pom_remove_dep :jetty-memcached-sessions jetty-home

# Hazelcast in Fedora is too old to build against
%pom_disable_module jetty-hazelcast
%pom_disable_module test-hazelcast-sessions tests/test-sessions
%pom_remove_dep :jetty-hazelcast jetty-home

# Infinispan in Fedora is too old to build against
%pom_disable_module jetty-infinispan
%pom_disable_module test-infinispan-sessions tests/test-sessions
%pom_remove_dep :infinispan-embedded jetty-home
%pom_remove_dep :infinispan-embedded-query jetty-home
%pom_remove_dep :infinispan-remote jetty-home
%pom_remove_dep :infinispan-remote-query jetty-home
%pom_xpath_remove "pom:execution[pom:id='unpack-infinispan-config']" jetty-home

# Springframework not available in Fedora
%pom_disable_module jetty-spring

# Not currently able to build tests, so can't build benchmarks
%pom_disable_module jetty-jmh

# Distribution tests require internet access, so disable
%pom_disable_module test-distribution tests

# missing conscrypt
%pom_disable_module jetty-alpn-conscrypt-server jetty-alpn
%pom_disable_module jetty-alpn-conscrypt-client jetty-alpn
%pom_remove_dep -r :jetty-alpn-conscrypt-server
%pom_remove_dep -r :jetty-alpn-conscrypt-client
rm -fr examples/embedded/src/main/java/org/eclipse/jetty/embedded/ManyConnectors.java

cp %{SOURCE6} .

# the default location is not allowed by SELinux
sed -i '/<SystemProperty name="jetty.state"/d' \
    jetty-home/src/main/resources/etc/jetty-started.xml

%if %{with jp_minimal}
# remote-resources only copies about.html
%pom_remove_plugin :maven-remote-resources-plugin
# packages module configs, we don't need those in minimal
%pom_remove_plugin :maven-assembly-plugin
# only useful when tests are enabled (copies test deps)
%pom_remove_plugin :maven-dependency-plugin jetty-client

%pom_disable_module jetty-ant
%pom_disable_module jetty-http2
%pom_disable_module jetty-fcgi
%pom_disable_module jetty-websocket
%pom_disable_module jetty-servlets
%pom_disable_module jetty-util-ajax
%pom_disable_module apache-jsp
%pom_disable_module apache-jstl
%pom_disable_module jetty-maven-plugin
%pom_disable_module jetty-jspc-maven-plugin
%pom_disable_module jetty-deploy
%pom_disable_module jetty-start
%pom_disable_module jetty-plus
%pom_disable_module jetty-annotations
%pom_disable_module jetty-jndi
%pom_disable_module jetty-cdi
%pom_disable_module jetty-proxy
%pom_disable_module jetty-jaspi
%pom_disable_module jetty-rewrite
%pom_disable_module jetty-nosql
%pom_disable_module jetty-unixsocket
%pom_disable_module tests
%pom_disable_module examples
%pom_disable_module jetty-quickstart
%pom_disable_module jetty-distribution
%pom_disable_module jetty-runner
%pom_disable_module jetty-http-spi
%pom_disable_module jetty-alpn
%pom_disable_module jetty-home
%pom_disable_module jetty-openid

%endif

%build
%mvn_package :jetty-home __noinstall
%mvn_package :jetty-distribution __noinstall
%mvn_package :build-resources __noinstall

# Separate package for POMs
%if %{without jp_minimal}
%mvn_package ':*-project' project
%mvn_package ':*-parent' project
%mvn_package ':*-bom' project
%else
%mvn_package ':*-project' __noinstall
%mvn_package ':*-parent' __noinstall
%mvn_package ':*-bom' __noinstall
%endif

# artifact used by demo
%mvn_package :test-mock-resources

%mvn_package ':test-*' __noinstall
%mvn_package ':*-tests' __noinstall
%mvn_package ':*-it' __noinstall
%mvn_package ':example-*' __noinstall
%mvn_package org.eclipse.jetty.tests: __noinstall
%mvn_package ::war: __noinstall
%mvn_package :jetty-runner __noinstall

%mvn_package org.eclipse.jetty.cdi: jetty-cdi

%mvn_package ':jetty-alpn*-client' jetty-alpn-client
%mvn_package ':jetty-alpn*-server' jetty-alpn-server


%mvn_package :apache-jsp jetty-jsp
%mvn_alias :apache-jsp :jetty-jsp

# we don't have all necessary dependencies to run tests
# missing test dep: org.eclipse.jetty.toolchain:jetty-perf-helper
%mvn_build -f -s


%install
%mvn_install

# jp_minimal version doesn't contain main package
%if %{without jp_minimal}
# Install jetty home
cp -pr jetty-distribution/target/distribution %{buildroot}%{homedir}

# dirs
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -dm 755 %{buildroot}%{confdir}
install -dm 755 %{buildroot}%{homedir}/start.d
install -dm 755 %{buildroot}%{logdir}
install -dm 755 %{buildroot}%{rundir}
install -dm 755 %{buildroot}%{tempdir}
install -dm 755 %{buildroot}%{jettylibdir}
install -dm 755 %{buildroot}%{_unitdir}

# systemd unit file
cp %{SOURCE5} %{buildroot}%{_unitdir}/

install -pm 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
echo '# Placeholder configuration file.  No default is provided.' > \
     %{buildroot}%{confdir}/jetty.conf

# add dependencies that are missing due to artifact coordinates changes
build-jar-repository %{buildroot}%{homedir}/lib/apache-jsp \
           tomcat/jasper tomcat/tomcat-juli \
           tomcat/tomcat-jsp-2.3-api tomcat/tomcat-api tomcat/tomcat-util \
           tomcat-taglibs-standard/taglibs-standard-compat \
           tomcat-taglibs-standard/taglibs-standard-impl \
           tomcat/tomcat-util-scan glassfish-el-api glassfish-el

# ecj doesn't have javapackages metadata in manifest, remove when fixed
ecj=`echo %{buildroot}%{homedir}/lib/apache-jsp/org.eclipse.jdt.ecj-*.jar`
rm $ecj

# substitute dependency jars (keep start.jar with shaded jetty util)
xmvn-subst -s -L -R %{buildroot} %{buildroot}%{homedir}/lib

# ecj doesn't have javapackages metadata in manifest, remove when fixed
ln -sf %{_javadir}/ecj.jar $ecj

# TODO uncomment when jetty-setuid is packaged
# test -e %{_jnidir}/jetty-setuid/libsetuid-linux.so
# ln -sf %{_jnidir}/jetty-setuid/libsetuid-linux.so %{buildroot}%{homedir}/lib/setuid/

( cat << EO_RC
JAVA_HOME="%{java_home}"
JAVA_OPTIONS=
JETTY_HOME=%{homedir}
JETTY_CONSOLE=%{logdir}/jetty-console.log
JETTY_PORT=8080
JETTY_RUN=%{_localstatedir}/run/%{name}
JETTY_PID=\$JETTY_RUN/jetty.pid
EO_RC
) > %{buildroot}%{homedir}/.jettyrc

mkdir -p %{buildroot}%{_tmpfilesdir}
( cat << EOF
D %{rundir} 0755 %username %{username} -
EOF
) > %{buildroot}%{_tmpfilesdir}/%{name}.conf

rm -r %{buildroot}%{homedir}/logs
ln -s %{logdir} %{buildroot}%{homedir}/logs

mv %{buildroot}%{homedir}/etc/* %{buildroot}/%{confdir}/
rm -r %{buildroot}%{homedir}/etc
ln -s %{confdir} %{buildroot}%{homedir}/etc

mv %{buildroot}%{homedir}/webapps %{buildroot}%{appdir}
ln -s %{appdir} %{buildroot}%{homedir}/webapps

rm %{buildroot}%{homedir}/*.txt  %{buildroot}%{homedir}/*.html

# Here jetty is going to put its runtime data.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=845993
ln -sf %{rundir} %{buildroot}%{homedir}/work

# replace the startup script with ours
cp -p %{SOURCE1} %{buildroot}%{homedir}/bin/jetty.sh

# NOTE: %if %{without jp_minimal} still in effect

%pre
# Add the "jetty" user and group
getent group %username >/dev/null || groupadd -f -g %jtuid -r %username
if ! getent passwd %username >/dev/null ; then
    if ! getent passwd %jtuid >/dev/null ; then
      useradd -r -u %jtuid -g %username -d %homedir -s /usr/sbin/nologin \
      -c "Jetty web server" %username
    else
      useradd -r -g %username -d %homedir -s /usr/sbin/nologin \
      -c "Jetty web server" %username
    fi
fi
exit 0

%post
%systemd_post jetty.service

%preun
%systemd_preun jetty.service

%postun
%systemd_postun_with_restart jetty.service


%endif

%files client -f .mfiles-jetty-client
%files continuation -f .mfiles-jetty-continuation
%files jaas -f .mfiles-jetty-jaas
%files io -f .mfiles-jetty-io
%files server -f .mfiles-jetty-server
%files servlet -f .mfiles-jetty-servlet
%files util -f .mfiles-jetty-util
%license LICENSE NOTICE.txt LICENSE-MIT
%files webapp -f .mfiles-jetty-webapp
%files jmx -f .mfiles-jetty-jmx
%files xml -f .mfiles-jetty-xml
%files http -f .mfiles-jetty-http
%files security -f .mfiles-jetty-security

%if %{with jp_minimal}
%files
# Empty metapackage in minimal mode
%endif

%if %{without jp_minimal}
%files -f .mfiles
%{_tmpfilesdir}/%{name}.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{confdir}
%dir %{jettylibdir}
%dir %{jettycachedir}
%{homedir}
%attr(744, jetty, jetty) %{homedir}/bin/jetty.sh
%attr(755, jetty, jetty) %{logdir}
%attr(755, jetty, jetty) %{tempdir}
%ghost %dir %attr(755, jetty, jetty) %{rundir}
%{appdir}
%{_unitdir}/%{name}.service

%files project -f .mfiles-project
%doc README.md VERSION.txt
%license LICENSE NOTICE.txt LICENSE-MIT

%files annotations -f .mfiles-jetty-annotations
%files ant -f .mfiles-jetty-ant
%files cdi -f .mfiles-jetty-cdi
%files deploy -f .mfiles-jetty-deploy
%files fcgi-client -f .mfiles-fcgi-client
%files fcgi-server -f .mfiles-fcgi-server
%files http-spi -f .mfiles-jetty-http-spi
%files jaspi -f .mfiles-jetty-jaspi
%files jndi -f .mfiles-jetty-jndi
%files jsp -f .mfiles-jetty-jsp
%files jstl -f .mfiles-apache-jstl
%files jspc-maven-plugin -f .mfiles-jetty-jspc-maven-plugin
%files maven-plugin -f .mfiles-jetty-maven-plugin
%files plus -f .mfiles-jetty-plus
%files proxy -f .mfiles-jetty-proxy
%files quickstart -f .mfiles-jetty-quickstart
%files rewrite -f .mfiles-jetty-rewrite
%files servlets -f .mfiles-jetty-servlets
%files start -f .mfiles-jetty-start
%files unixsocket -f .mfiles-jetty-unixsocket
%files util-ajax -f .mfiles-jetty-util-ajax
%files websocket-api -f .mfiles-websocket-api
%files websocket-client -f .mfiles-websocket-client
%files websocket-common -f .mfiles-websocket-common
%files websocket-server -f .mfiles-websocket-server
%files websocket-servlet -f .mfiles-websocket-servlet
%files javax-websocket-client-impl -f .mfiles-javax-websocket-client-impl
%files javax-websocket-server-impl -f .mfiles-javax-websocket-server-impl
%files alpn-client -f .mfiles-jetty-alpn-client
%files alpn-server -f .mfiles-jetty-alpn-server
%files http2-client -f .mfiles-http2-client
%files http2-common -f .mfiles-http2-common
%files http2-hpack -f .mfiles-http2-hpack
%files http2-http-client-transport -f .mfiles-http2-http-client-transport
%files http2-server -f .mfiles-http2-server
%files nosql -f .mfiles-jetty-nosql
%endif

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE.txt LICENSE-MIT

%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.4.31-4
- License verified.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.4.31-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Thu Aug 13 2020 Mat Booth <mat.booth@redhat.com> - 9.4.31-2
- Reflective use of classes that might not be present in the JDK should be
  optional when expressed as OSGi dependencies

* Wed Aug 12 2020 Mat Booth <mat.booth@redhat.com> - 9.4.31-1
- Update to latest upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.30-3.v20200611
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 9.4.30-2.v20200611
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 18 2020 Mat Booth <mat.booth@redhat.com> - 9.4.30-1.v20200611
- Update to latest upstream release

* Fri Mar 20 2020 Mat Booth <mat.booth@redhat.com> - 9.4.27-1.v20200227
- Update to latest upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.24-3.v20191120
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Mat Booth <mat.booth@redhat.com> - 9.4.24-2.v20191120
- Switch to minimal build. There are too many missing deps for a full build

* Thu Nov 28 2019 Mat Booth <mat.booth@redhat.com> - 9.4.24-1.v20191120
- Update to latest release
- Drop spring module due to missing deps

* Mon Sep 02 2019 Mat Booth <mat.booth@redhat.com> - 9.4.20-1
- Update to latest upstream release
- Obsolete left-over packages that would have broken deps when built in minimal mode

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.19-2.v20190610
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Mat Booth <mat.booth@redhat.com> - 9.4.19-1.v20190610
- Update to latest upstream release

* Tue Jun 11 2019 Mat Booth <mat.booth@redhat.com> - 9.4.18-3.v20190429
- Fix license tags

* Fri May 03 2019 Mat Booth <mat.booth@redhat.com> - 9.4.18-2.v20190429
- Remove dep on Eclipse since it's not available on all platforms, and don't
  ship OSGi modules

* Wed May 01 2019 Mat Booth <mat.booth@redhat.com> - 9.4.18-1.v20190429
- Update to latest upstream release
- Remove some ancient obsoletes

* Thu Apr 25 2019 Mat Booth <mat.booth@redhat.com> - 9.4.17-1.v20190418
- Update to latest upstream release
- Stop building and obsolete the infinispan module

* Tue Feb 19 2019 Mat Booth <mat.booth@redhat.com> - 9.4.15-1.v20190215
- Update to latest upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.14-2.v20181114
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Mat Booth <mat.booth@redhat.com> - 9.4.14-1.v20181114
- Update to upstream version 9.4.14.v20181114
- Stop building and obsolete the hazelcast module
- Fixup the license tag

* Fri Aug 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 9.4.11-4.v20180605
- Add explicit requirement on javapackages-tools for jetty.sh.
  See RHBZ#1600426.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.11-3.v20180605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Michael Simacek <msimacek@redhat.com> - 9.4.11-2.v20180605
- Fix missing classes in start.jar

* Fri Jun 08 2018 Michael Simacek <msimacek@redhat.com> - 9.4.11-1.v20180605
- Update to upstream version 9.4.11.v20180605

* Wed May 09 2018 Michael Simacek <msimacek@redhat.com> - 9.4.10-1.v20180503
- Update to upstream version 9.4.10.v20180503

* Mon Apr 30 2018 Michael Simacek <msimacek@redhat.com> - 9.4.10-0.1.RC1
- Update to upstream version 9.4.10.RC1

* Fri Mar 23 2018 Mat Booth <mat.booth@redhat.com> - 9.4.9-2.v20180320
- Make the requirement on "osgi.serviceloader.processor" optional

* Wed Mar 21 2018 Alexander Kurtakov <akurtako@redhat.com> 9.4.9-1.v20180320
- Update to upstream 9.4.9 release.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9.4.8-4.v20171121
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.8-3.v20171121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Michael Simacek <msimacek@redhat.com> - 9.4.8-2.v20171121
- Remove obsolete systemd conversion scriptlet

* Mon Dec 04 2017 Michael Simacek <msimacek@redhat.com> - 9.4.8-1.v20171121
- Update to upstream version 9.4.8.v20171121

* Wed Sep 20 2017 Michael Simacek <msimacek@redhat.com> - 9.4.7-1.v20170914
- Update to upstream version 9.4.7.v20170914

* Wed Sep 13 2017 Michael Simacek <msimacek@redhat.com> - 9.4.7.RC0-1
- Update to upstream version 9.4.7.RC0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.6-2.v20170531
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Michael Simacek <msimacek@redhat.com> - 9.4.6-1.v20170531
- Update to upstream version 9.4.6.v20170531

* Thu May 04 2017 Michael Simacek <msimacek@redhat.com> - 9.4.5-1.v20170502
- Update to upstream version 9.4.5.v20170502

* Wed Apr 19 2017 Michael Simacek <msimacek@redhat.com> - 9.4.4-1.v20170414
- Update to upstream version 9.4.4.v20170414

* Fri Apr 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.4.3-3.v20170317
- Fix installation of webapps directory
- Resolves: rhbz#1442334

* Wed Apr  5 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.4.3-2.v20170317
- Make the requirement on "osgi.serviceloader.registrar" optional
- Resolves: rhbz#1427189

* Tue Mar 28 2017 Michael Simacek <msimacek@redhat.com> - 9.4.3-1.v20170317
- Update to upstream version 9.4.3.v20170317

* Thu Mar 16 2017 Michael Simacek <msimacek@redhat.com> - 9.4.2-3.v20170220
- Rework conditionals
- Switch jsp provider to glassfish - it's newer

* Tue Mar 07 2017 Michael Simacek <msimacek@redhat.com> - 9.4.2-2.v20170220
- Make the requirement on "osgi.serviceloader.processor" optional
- Resolves: rhbz#1427189

* Fri Feb 24 2017 Michael Simacek <msimacek@redhat.com> - 9.4.2-1.v20170220
- Update to upstream version 9.4.2.v20170220

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 9.4.1-6.v20170120
- Remove release-plugin from build

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 9.4.1-5.v20170120
- Add conditional for weld

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 9.4.1-4.v20170120
- Add conditionals for nosql, spring and equinox

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.4.1-3.v20170120
- Introduce infinispan build conditional

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 9.4.1-2.v20170120
- Fix FTBFS

* Tue Jan 24 2017 Michael Simacek <msimacek@redhat.com> - 9.4.1.v20170120
- Update to upstream version 9.4.1.v20170120

* Fri Dec 09 2016 Michael Simacek <msimacek@redhat.com> - 9.4.0-1.v20161208
- Update to upstream version 9.4.0.v20161208

* Tue Sep 20 2016 Michael Simacek <msimacek@redhat.com> - 9.4.0-0.3.RC2
- Update to upstream version 9.4.0.RC2
- Version Obsoletes
- Reorganize packaging of POM files
- Use xmvn-subst to replace symlinks
- Enable test and example modules

* Thu Jun 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.4.0-0.2.M0
- Add missing build-requires

* Mon Jun 06 2016 Michael Simacek <msimacek@redhat.com> - 9.4.0-0.1.M0
- Update to upstream version 9.4.0.M0

* Wed Jun 01 2016 Michael Simacek <msimacek@redhat.com> - 9.3.10-0.1.M0
- Update to upstream version 9.3.10.M0

* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.9-0.2.M0
- Fix build issue with maven-jar-plugin 3.0.0

* Mon Apr 11 2016 Michael Simacek <msimacek@redhat.com> - 9.3.9-0.1.M0
- Update to upstream version 9.3.9.M0

* Thu Mar 24 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.8-1.v20160314
- Update to upstream version 9.3.8.v20160314

* Mon Feb 29 2016 Michael Simacek <msimacek@redhat.com> - 9.3.8-0.1RC0
- Update to upstream version 9.3.8.RC0

* Fri Feb 19 2016 Michael Simacek <msimacek@redhat.com> - 9.3.7-2.v20160115
- Use %%_tmpfilesdir
- Resolves: rhbz#1289494
- Fix changelog

* Mon Feb 15 2016 Michael Simacek <msimacek@redhat.com> - 9.3.7-1.v20160115
- Update to upstream version 9.3.7.v20160115
- Port to current mongo-java-driver

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.7-0.3.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Michael Simacek <msimacek@redhat.com> - 9.3.7-0.2.RC1
- Update to RC1

* Fri Jan 08 2016 Michael Simacek <msimacek@redhat.com> - 9.3.7-0.1.RC0
- Update to upstream version 9.3.7.RC0

* Fri Nov 20 2015 Michael Simacek <msimacek@redhat.com> - 9.3.6-1
- Update to upstream version 9.3.6.v20151106

* Fri Oct  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.4-1
- Update to upstream version 9.3.4

* Tue Sep 01 2015 Michael Simacek <msimacek@redhat.com> - 9.3.3-1
- Update to upstream version 9.3.3.v20150827
- Remove manual requires on glassfish-servlet-api as the duplicate provides
  were fixed

* Mon Aug 03 2015 Michael Simacek <msimacek@redhat.com> - 9.3.2-1
- Update to upstream version 9.3.2.v20150730

* Thu Jul 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.1-1
- Update to upstream version 9.3.1

* Fri Jul 03 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0-6
- Remove BR on eclipse-rcp

* Mon Jun 22 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0-5
- Update to upstream release 0.3.0.v20150612

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0-3
- Improve packaging

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0-2
- Add alias for jetty-jsp

* Tue Mar 24 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0-1
- Update to upstream version 9.3.0
- Fix symlinks

* Tue Mar 17 2015 Michael Simacek <msimacek@redhat.com> - 9.2.9-3
- Use report goal of maven-plugin-plugin instead of xdoc

* Thu Mar 5 2015 Alexander Kurtakov <akurtako@redhat.com> 9.2.9-2
- Rebuild against tomcat-taglibs-standard.

* Wed Feb 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.2.9-1
- Update to upstream version 9.2.9
- Resolves: CVE-2015-2080

* Thu Jan 22 2015 Michael Simacek <msimacek@redhat.com> - 9.2.7-1
- Update to upstream version 9.2.7

* Thu Dec 11 2014 Michael Simacek <msimacek@redhat.com> - 9.2.6-3
- Update to upstream version 9.2.6
- Simplify symlink creation
- Include symlink to jetty-schemas (RHBZ#1170829)
- Set glassfish as default jsp implementation

* Fri Oct 10 2014 Michael Simacek <msimacek@redhat.com> - 9.2.3-2
- Add missing requires jetty-start

* Wed Sep 10 2014 Michael Simacek <msimacek@redhat.com> - 9.2.3-1
- Update to upstream version 9.2.3

* Tue Jul 29 2014 Michael Simacek <msimacek@redhat.com> - 9.2.2-1
- Update to upstream version 9.2.2

* Fri Jun 13 2014 Michael Simacek <msimacek@redhat.com> - 9.2.1-1
- Update to upstream version 9.2.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Michael Simacek <msimacek@redhat.com> - 9.2.0-1
- Update to upstream version 9.2.0

* Tue May 06 2014 Michael Simacek <msimacek@redhat.com> - 9.1.5-1
- Update to upstream version 9.1.5

* Fri Apr 11 2014 Michael Simacek <msimacek@redhat.com> - 9.1.4-3
- Remove jetty-runner subpackage

* Thu Apr 10 2014 Michael Simacek <msimacek@redhat.com> - 9.1.4-2
- Install startup script into correct directory
- Add a notice about httpd_execmem into the startup script

* Tue Apr 08 2014 Michael Simacek <msimacek@redhat.com> - 9.1.4-1
- Update to upstream version 9.1.4

* Tue Apr 01 2014 Michael Simacek <msimacek@redhat.com> - 9.1.3-4
- Simplify (and fix) jetty startup script and use systemd features

* Thu Mar 06 2014 Erinn Looney-Triggs <erinn.looneytriggs@gmail.com> - 9.1.3-3
- Adjust useradd to be more flexible as shown here:
  https://fedoraproject.org/wiki/Packaging:UsersAndGroups

* Thu Mar 06 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 9.1.3-2
- Use Requires: java-headless rebuild (#1067528)

* Tue Mar 04 2014 Michael Simacek <msimacek@redhat.com> - 9.1.3-1
- Update to upstream version 9.1.3

* Fri Feb 28 2014 Michael Simacek <msimacek@redhat.com> - 9.1.2-2
- Remove JARs bundled in main package

* Wed Feb 12 2014 Michael Simacek <msimacek@redhat.com> - 9.1.2-1
- Update to upstream version 9.1.2
- Remove subpackage websocket-mux-extension (unstable, removed upstream)

* Fri Jan 10 2014 Michael Simacek <msimacek@redhat.com> - 9.1.1-1
- Update to upstream version 9.1.1
- Install .mod files

* Thu Dec 19 2013 Michael Simacek <msimacek@redhat.com> - 9.1.0-4
- Add missing BD on ecj

* Thu Dec 19 2013 Michael Simacek <msimacek@redhat.com> - 9.1.0-3
- Replace dependency patch with pom_editor macro calls
- Drop unnecessary dependency on tomcat-jasper and BR on tomcat-lib

* Wed Dec 18 2013 Michael Simacek <msimacek@redhat.com> - 9.1.0-2
- Symlink to glassfish-servlet-api instead of tomcat

* Wed Nov 27 2013 Michael Simacek <msimacek@redhat.com> - 9.1.0-1
- Update to upstream version 9.1.0

* Fri Oct 11 2013 Michal Srb <msrb@redhat.com> - 9.0.6-1
- Update to upstream version 9.0.6
- Install licenses with jetty-util subpackage

* Sat Sep 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.5-2
- Move configuration directories to %%{_sysconfdir}
- Resolves: rhbz#596611

* Thu Aug 22 2013 Michal Srb <msrb@redhat.com> - 9.0.5-1
- Update to upstream version 9.0.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Michal Srb <msrb@redhat.com> - 9.0.4-1
- Update to upstream version 9.0.4

* Wed Jun 26 2013 Michal Srb <msrb@redhat.com> - 9.0.3-4
- Add missing BR: maven-plugin-build-helper
- Add MIT license text
- Don't install CDDL license
- More specific explanation why tests are disabled

* Wed May 29 2013 Michal Srb <msrb@redhat.com> - 9.0.3-3
- Add description for jetty-util

* Thu May 23 2013 Michal Srb <msrb@redhat.com> - 9.0.3-2
- Obsolete old jetty-websocket subpackage (Resolves: #966352)

* Thu May 09 2013 Michal Srb <msrb@redhat.com> - 9.0.3-1
- Update to upstream version 9.0.3

* Mon Apr 22 2013 Michal Srb <msrb@redhat.com> - 9.0.2-1
- Update to upstream version 9.0.2

* Thu Apr 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.0-3
- Remove maven-license-plugin
- Conditionally disable jetty-spring
- Fix OSGi conditionals

* Wed Apr 10 2013 Michal Srb <msrb@redhat.com> - 9.0.0-2
- Replace tomcat libs with glassfish libs
- Add ability to build package without service files
- Remove unneeded ecj custom depmap

* Wed Mar 13 2013 Michal Srb <msrb@redhat.com> - 9.0.0-1
- Update to upstream version 9.0.0

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.0-0.4.RC3
- Add missing BR: glassfish-el

* Mon Mar  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.0-0.3.RC3
- Update to Jetty 9 RC3

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.0-0.2.RC2
- Upload sources for Jetty 9 RC2

* Thu Feb 28 2013 Michal Srb <msrb@redhat.com> - 9.0.0-0.2.RC2
- Update to 9.0.0.RC2

* Fri Feb 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.0-0.1.RC0
- Remove duplicated %%files for javadoc package
- Add the new tarball to sources

* Mon Feb 18 2013 Michal Srb <msrb@redhat.com> - 9.0.0-0.1.RC0
- Update to upstream version 9.0.0
- Build with xmvn

* Fri Feb 15 2013 Alexander Kurtakov <akurtako@redhat.com> 8.1.9-3
- Add missing BR on maven-license-plugin.

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.9-2
- Update upstream URL
- Resolves: rhbz#911292

* Thu Feb 14 2013 Alexander Kurtakov <akurtako@redhat.com> 8.1.9-1
- Update to 8.1.9.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 8.1.5-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Dec 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.5-10
- Reenable osgi support

* Mon Nov  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.5-9
- Use file lists generated by improved add_maven_depmap macro

* Wed Oct 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-8
- Fix build conditionals

* Tue Oct  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-7
- Introduce nosql and osgi conditionals
- Temporarly disable osgi to bootstrap eclipse

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-6
- Don't delete jetty user on package erase, resolves: rhbz#857708

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-5
- Create work directory if not exists

* Tue Aug 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-4
- Convert systemd scriplets to macros, resolves #850176

* Tue Aug 21 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-3
- Don't redirect useradd and groupadd output to the bit bucket

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-2
- Put runtime data in /run instead of /tmp
- Fix patch for disabling OSGi

* Wed Jul 18 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.5-1
- Update to upstream version 8.1.5
- Fix rpmlint warnings

* Wed Jul 18 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.4-3
- Disable SPDY to fix FTBFS

* Wed Jun 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.4-2
- Fix jetty being accidentaly enabled after update by default
- Resolves: #831280

* Tue May 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.4-1
- Update to 8.1.4

* Thu May 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.2-9
- Add patch to disable jetty-nosql

* Wed May 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.2-8
- Build jetty-nosql conditionally

* Tue May 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.2-7
- Add unconditional BR on glassfish-jsp to make build-jar-repository work

* Wed May  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.2-6
- Move start.ini to /etc
- Require glassfish-jsp only for jetty-webapp and jetty-osgi
- Use shadow-utils directly instead of fedora-usermgmt-devel
- Fix license tags

* Mon Apr 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.2-5
- Don't require subpackages not needed by server itself
- Make jetty look for jars in correct directory
- Add proper dependent jars

* Fri Apr 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.2-4
- Keep license files only in jetty-project and jetty-javadoc packages

* Fri Apr 27 2012 Alexander Kurtakov <akurtako@redhat.com> 8.1.2-3
- There is no epoch define in jetty.

* Thu Apr 26 2012 Alexander Kurtakov <akurtako@redhat.com> 8.1.2-2
- Drop envr from jpackage-utils as it was wrong.

* Thu Apr 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.2-1
- Update to 8.1.2 upstream release

* Wed Apr 25 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.0-7
- Split into number of subpackages

* Mon Apr 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.0-6
- Drop init script, resolves #814788
- Remove jetty.script from SCM
- Reload systemd on package install/upgrade/remove

* Wed Apr 18 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.1.0-5
- Replace eclipse-rcp BR with felix-framework
- Add missing R: felix-framework

* Fri Feb 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-4
- Add geronimo-annotation to Requires

* Thu Feb 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-3
- Fix web server running example webapp
- Add systemd unit file and conversion scriptlets

* Wed Feb 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-2
- Fix #794913 - missing user management utils during install

* Wed Feb  1 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-1
- Update to final release

* Mon Jan 30 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-0.4.rc5
- Fix upgrade path problems
- Symlink conf files into etc (so users still see them there)

* Thu Jan 26 2012 Alexander Kurtakov <akurtako@redhat.com> 8.1.0-0.3.rc5
- Revert the dependency on jetty-parent - we don't need the whole maven stack when installing jetty.
- Make the javadoc package not depend on the main one.

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-0.2.rc5
- Add jetty-parent to Requires

* Wed Jan 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-0.1.rc5
- Update to rc5
- Remove symbolic name patch (not needed after bundle plugin fix)

* Wed Jan 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 8.1.0-0.1.RC4
- Major update to 8.1.0 RC4
- Removed manual subpackage (was empty anyway)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Alexander Kurtakov <akurtako@redhat.com> 6.1.26-8
- Install jetty-client and its deps into _javadir and provide maven integration.

* Tue Jun 28 2011 Alexander Kurtakov <akurtako@redhat.com> 6.1.26-7
- Adapt build for maven 3.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Alexander Kurtakov <akurtako@redhat.com> 6.1.26-5
- Do not require tomcat6-lib.
- Drop one depmap.

* Tue Dec 14 2010 Alexander Kurtakov <akurtako@redhat.com> 6.1.26-4
- Do not require apache-commons-parent in order to not bring maven and friends.

* Wed Dec 01 2010 Jeff Johnston <jjohnstn@redhat.com> 6.1.26-3
- Resolves #655808
- Fix util pom to reference javax.servlet groupid for servlet-api.
- Don't add tomcat6-servlet-api to depmap.
- Remove tomcat5 BR.

* Mon Nov 22 2010 Jeff Johnston <jjohnstn@redhat.com> 6.1.26-2
- Resolves #652020
- Remove tomcat5 references and replace with appropriate alternatives.

* Fri Nov 12 2010 Alexander Kurtakov <akurtako@redhat.com> 6.1.26-1
- Update to 6.1.26.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 6.1.24-1
- Update to 6.1.24.

* Wed Dec 02 2009 Jeff Johnston <jjohnstn@redhat.com> 6.1.21-4
- Resolves #543081
- Add maven depmap fragments.

* Tue Nov 03 2009 Jeff Johnston <jjohnstn@redhat.com> 6.1.21-3
- Security issues
- Resolves #532675, #5326565

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 6.1.21-2
- Install unversioned jars.

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 6.1.21-1
- Update to upstream 6.1.21 release.

* Fri Sep 18 2009 Jeff Johnston <jjohnstn@redhat.com> 6.1.20-3
- Add djetty script source and fix init script to work properly.

* Tue Sep 15 2009 Alexander Kurtakov <akurtako@redhat.com> 6.1.20-2
- Fix requires.

* Tue Sep 15 2009 Alexander Kurtakov <akurtako@redhat.com> 6.1.20-1
- Update to upstream 6.1.20.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.15-3
- Do not allow directory listings.

* Tue May 19 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.15-2
- Update OSGI manifest file.

* Tue May 19 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.15-1
- Upgrade to 5.1.15 source tarball for Fedora.

* Wed Apr 22 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-3
- Add %%{libdir} to files list.
- Resolves #473585

* Wed Feb 11 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1.10
- Rename jettyc back to .jettyrc.
- Resolves #485012

* Tue Feb 03 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1.9
- Change %%{_sysconfdir}/init.d references to be %%{_initrddir}

* Mon Feb 02 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1.8
- Fixes for unowned directories.

* Tue Jan 06 2009 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1.7
- Patch init.d script to add status operation
- Patch unix djetty script so it doesn't issue error messages about /dev/tty
  and fix various inconsistencies with the init.d script

* Tue Aug 12 2008 Andrew Overholt <overholt@redhat.com> 5.1.14-1.6
- Require tomcat5 bits with proper OSGi metadata

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 5.1.14-1.5
- Bump release.

* Fri Jul 11 2008 Andrew Overholt <overholt@redhat.com> 5.1.14-1.3
- Update OSGi manifest

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.1.14-1.3
- drop repotag

* Fri Jul 04 2008 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1jpp.2
- Security patch
- Resolves #417401, #417411, #417391

* Wed Jun 25 2008 Jeff Johnston <jjohnstn@redhat.com> 5.1.14-1jpp.1
- Upgrade to 5.1.14 source tarball for Fedora

* Fri Aug 31 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.7
- Resolves #262221
- Use /bin/sh instead of /sbin/nologin so init will work

* Thu Aug 30 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.6
- Rename all source files from jetty5 to jetty
- Replace jetty5 references with jetty in source files

* Tue Aug 28 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.5
- Rename from jetty5 to jetty

* Mon Aug 27 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.4
- Remove post manual step
- Remove jsse requirement
- Add comment inside jetty.conf so it isn't empty

- Use /sbin/nologin when creating the jetty5 user and group
* Mon Aug 27 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.3
- Use /sbin/nologin when creating the jetty5 user and group
- Remove all jars in %%prep
- Remove unnecessary preun step for removing extra jars
- Fix license
- Fix group for manual subpackage
- Fix group for javadoc subpackage
- Add comment regarding empty jetty.conf file
- Add jsp requirement
- Remove %%post javadoc ln command
- Remove %%post manual ln command
- Change source0 tarball to remove BCLA-licensed jars
- Remove epoch 0 references in subpackage requires for extras and manual
- Rename .jettyrc to jettyrc
- Remove hidden files
- Don't install gcj files twice

* Fri Aug 24 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.2
- Remove demo subpackage.

* Wed Aug 08 2007 Jeff Johnston <jjohnstn@redhat.com> 5.1.12-1jpp.1
- Comment out demo subpackage.

* Mon Aug 06 2007 Ben Konrath <bkonrath@redhat.com> 5.1.12-1jpp.1
- Add --excludes to aot-compile-rpm line.
- Inject OSGi manifest into jetty jar.

* Thu Jul 19 2007 Andrew Overholt <overholt@redhat.com> 5.1.12-1jpp.1
- Update to 5.1.12 for Fedora.
- Use fedora-usermgmt stuff.

* Fri Feb 02 2007 Ralph Apel <r.apel at r-apel.de> - 0:5.1.12-1jpp
- Upgrade to 5.1.12
- Add gcj_support option
- Avoid circular dependency with mx4j-tools thru bootstrap option

* Sat Aug 12 2006 Anthony Green <green@redhat.com> - 0:5.1.11-0.rc0.4jpp
- Escape macros in changelog with %%.
- Untabify.
- Don't delete symlinks in %%preun.
- Add logrotate file.
- Don't install unversioned javadoc files.
- Don't rm old links in manual package.
- Convert some end-of-line encodings.

* Fri Aug 11 2006 Anthony Green <green@redhat.com> - 0:5.1.11-0.rc0.3jpp
- First Fedora build.
- Disable extras.
- Use fedora-useradd & fedora-userdel.
- Add gcj support.
- Tweak License and Group tags for rpmlint.
- Use full URL for Source0.

* Thu Aug 10 2006 Ralph Apel <r.apel@r-apel.de> - 0:5.1.11-0.rc0.2jpp
- Fix version/release in changelog
- Introduce option '--without extra' to omit this subpackage and its (B)Rs
- Don't delete user on erase
- Tidy up BRs
- Add commons-el.jar to ext
- No ghost for lib/org.mortbay.jetty.jar, lib/org.mortbay.jmx.jar
- Avoid use of build-jar-repository in spec
- Avoid use of rebuild-jar-repository in init and start script
- Don't handle JETTY_PID file in init script: start script takes care
- Patch PostFileFilter to remove a (unused) com.sun package import
- Explicitly (B)R  geronimo-jta-1.0.1B-api instead of any jta
- Add empty file /etc/jetty5/jetty.conf:
  activate contexts manually if desired

* Tue Jun 20 2006 Ralph Apel <r.apel@r-apel.de> - 0:5.1.2-3jpp
- First JPP-1.7 release

* Mon Mar 14 2005 Ralph Apel <r.apel@r-apel.de> - 0:5.1.2-2jpp
- link commons-logging to %%{_homedir}/ext
- link jspapi to %%{_homedir}/ext
- only use %%{_homedir}/etc not conf

* Tue Feb 01 2005 Ralph Apel <r.apel@r-apel.de> - 0:5.1.2-1jpp
- Upgrade to 5.1.2
- Prepare for build with Java 1.5, (thx to Petr Adamek)
- Require /sbin/chkconfig instead of chkconfig package

* Tue Jan 04 2005 Ralph Apel <r.apel@r-apel.de> - 0:5.0.0-2jpp
- Include build of extra, so called JettyPlus
- Create own subdirectory for jetty5 in %%{_javadir}
- Change %%{_homedir}/conf to %%{_homedir}/etc
- Dropped chkconfig requirement; just exec if /sbin/chkconfig available
- Fixed unpackaged .jettyrc

* Mon Oct 04 2004 Ralph Apel <r.apel@r-apel.de> - 0:5.0.0-1jpp
- Upgrade to 5.0.0
- Fixed URL
- relaxed some versioned dependencies

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:4.2.20-2jpp
- Rebuild with ant-1.6.2

* Fri Jun 18 2004 Ralph Apel <r.apel@r-apel.de> - 0:4.2.20-1jpp
- Upgrade to 4.2.20
- Drop ownership of /usr/share/java and /usr/bin

* Tue Feb 24 2004 Ralph Apel <r.apel@r-apel.de> - 0:4.2.17-2jpp
- enhancements and corrections thanks to Kaj J. Niemi:
- $JETTY_HOME/ext didn't exist but %%post depended on it
- correctly shutdown jetty upon uninstall
- RedHat depends on chkconfig/service to work so a functional
  init.d/jetty4 needed to be created
- djetty4 (jetty.sh) did funny things especially when it attempted to guess
  stuff
- a lot of .xml config files assumed that the configs were in etc/ instead of
  conf/

* Thu Feb 19 2004 Ralph Apel <r.apel@r-apel.de> - 0:4.2.17-1jpp
- First JPackage release.
