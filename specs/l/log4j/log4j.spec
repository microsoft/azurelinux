## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 25;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap
%bcond_without jp_minimal

Name:           log4j
Version:        2.20.0
Release:        %autorelease
Summary:        Java logging package
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch
License:        Apache-2.0

URL:            https://logging.apache.org/%{name}

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz

Patch:          logging-log4j-Remove-unsupported-EventDataConverter.patch
Patch:          0002-Remove-usage-of-toolchains.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.lmax:disruptor)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.mail:jakarta.mail-api)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.fusesource.jansi:jansi)
BuildRequires:  mvn(org.jctools:jctools-core)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif

%if %{without jp_minimal}
BuildRequires:  mvn(com.datastax.cassandra:cassandra-driver-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-xml)
BuildRequires:  mvn(com.fasterxml.jackson.dataformat:jackson-dataformat-yaml)
BuildRequires:  mvn(com.fasterxml.woodstox:woodstox-core)
BuildRequires:  mvn(com.lmax:disruptor)
BuildRequires:  mvn(jakarta.mail:jakarta.mail-api)
BuildRequires:  mvn(jakarta.servlet:jakarta.servlet-api)
BuildRequires:  mvn(javax.servlet.jsp:jsp-api)
BuildRequires:  mvn(org.apache.commons:commons-csv)
BuildRequires:  mvn(org.apache.logging:logging-parent:pom:)
BuildRequires:  mvn(org.apache.tomcat:tomcat-catalina)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.eclipse.persistence:javax.persistence)
BuildRequires:  mvn(org.fusesource.jansi:jansi:1)
BuildRequires:  mvn(org.jboss.spec.javax.jms:jboss-jms-api_1.1_spec)
BuildRequires:  mvn(org.jctools:jctools-core)
BuildRequires:  mvn(org.lightcouch:lightcouch)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-ext)
BuildRequires:  mvn(org.zeromq:jeromq)
BuildRequires:  mvn(sun.jdk:jconsole)

# Also needs:
# - Various Spring dependencies
# - javax.jms
# - io.fabric8.kubernetes-client
%endif

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.2.0-18

%description
Log4j is a tool to help the programmer output log statements to a
variety of output targets.

%package slf4j
Summary:        Binding between LOG4J 2 API and SLF4J

%description slf4j
Binding between LOG4J 2 API and SLF4J.

%package jcl
Summary:        Apache Log4j Commons Logging Bridge

%description jcl
Apache Log4j Commons Logging Bridge.

%package web
Summary:        Apache Log4j Web

%description web
Support for Log4j in a web servlet container.

%package bom
Summary:        Apache Log4j BOM

%description bom
Apache Log4j 2 Bill of Material

%if %{without jp_minimal}
%package osgi
Summary:        Apache Log4J Core OSGi Bundles

%description osgi
Apache Log4J Core OSGi Bundles.

%package taglib
Summary:        Apache Log4j Tag Library

%description taglib
Apache Log4j Tag Library for Web Applications.

%package jmx-gui
Summary:        Apache Log4j JMX GUI
Requires:       java-25-devel

%description jmx-gui
Swing-based client for remotely editing the log4j configuration and remotely
monitoring StatusLogger output. Includes a JConsole plug-in.

%package nosql
Summary:        Apache Log4j NoSql

%description nosql
Use NoSQL databases such as MongoDB and CouchDB to append log messages.
%endif

%prep
%autosetup -p1 -C

%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-site-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-toolchains-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r com.diffplug.spotless:spotless-maven-plugin
%pom_remove_plugin -r org.apache.logging.log4j:log4j-changelog-maven-plugin
%pom_remove_plugin -r org.codehaus.mojo:xml-maven-plugin

# remove all the stuff we'll build ourselves
find -name '*.jar' -o -name '*.class' -delete
rm -rf docs/api

%pom_disable_module %{name}-distribution
%pom_disable_module %{name}-samples

# Apache Flume is not in Fedora yet
%pom_disable_module %{name}-flume-ng

# artifact for upstream testing of log4j itself, shouldn't be distributed
%pom_disable_module %{name}-perf

%pom_remove_dep -r org.codehaus.groovy:groovy-bom
%pom_remove_dep -r com.fasterxml.jackson:jackson-bom
%pom_remove_dep -r jakarta.platform:jakarta.jakartaee-bom
%pom_remove_dep -r org.eclipse.jetty:jetty-bom
%pom_remove_dep -r org.junit:junit-bom
%pom_remove_dep -r io.fabric8:kubernetes-client-bom
%pom_remove_dep -r io.netty:netty-bom
%pom_remove_dep -r org.springframework:spring-framework-bom

# unavailable com.conversantmedia:disruptor
rm log4j-core/src/main/java/org/apache/logging/log4j/core/async/DisruptorBlockingQueueFactory.java
%pom_remove_dep -r com.conversantmedia:disruptor

# kafka not available
rm -r log4j-core/src/main/java/org/apache/logging/log4j/core/appender/mom/kafka
%pom_remove_dep -r :kafka-clients

%pom_remove_dep -r javax.jms:javax.jms-api

# we don't have commons-dbcp2
%pom_disable_module %{name}-jdbc-dbcp2

# We don't have mmongo-java
%pom_disable_module %{name}-mongodb3
%pom_disable_module %{name}-mongodb4

# System scoped dep provided by JDK
%pom_remove_dep :jconsole %{name}-jmx-gui
%pom_add_dep sun.jdk:jconsole %{name}-jmx-gui

# old AID is provided by felix, we want osgi-core
%pom_change_dep -r org.osgi:org.osgi.core org.osgi:osgi.core

# tests are disabled
%pom_remove_plugin :maven-failsafe-plugin

# Remove deps on slf4j-ext, it is no longer available in Fedora 35
%pom_remove_dep -r :slf4j-ext
%pom_remove_parent
%pom_remove_parent log4j-bom

# Make compiled code compatible with OpenJDK 8
%pom_xpath_inject 'pom:plugin[pom:artifactId="maven-compiler-plugin"]/pom:configuration' "<release>8</release>"

%pom_disable_module %{name}-api-test
%pom_disable_module %{name}-core-test
%pom_disable_module %{name}-layout-template-json-test
%pom_disable_module %{name}-slf4j2-impl

%if %{with jp_minimal}
%pom_disable_module %{name}-taglib
%pom_disable_module %{name}-jmx-gui
%pom_disable_module %{name}-jakarta-web
%pom_disable_module %{name}-iostreams
%pom_disable_module %{name}-jul
%pom_disable_module %{name}-core-its
%pom_disable_module %{name}-jpa
%pom_disable_module %{name}-couchdb
%pom_disable_module %{name}-cassandra
%pom_disable_module %{name}-appserver
%pom_disable_module %{name}-spring-cloud-config
%pom_disable_module %{name}-spring-boot
%pom_disable_module %{name}-docker
%pom_disable_module %{name}-kubernetes
%pom_disable_module %{name}-layout-template-json

%pom_remove_dep -r :jackson-core
%pom_remove_dep -r :jackson-databind
%pom_remove_dep -r :jackson-dataformat-yaml
%pom_remove_dep -r :jackson-dataformat-xml
%pom_remove_dep -r :woodstox-core
%pom_remove_dep -r :jeromq
%pom_remove_dep -r :commons-csv

rm -r log4j-core/src/main/java/org/apache/logging/log4j/core/{jackson,config/yaml,config/json,parser}
rm -r log4j-core/src/main/java/org/apache/logging/log4j/core/appender/{db,mom,nosql}
rm log4j-core/src/main/java/org/apache/logging/log4j/core/layout/*{Csv,Jackson,Xml,Yaml,Json,Gelf}*.java
rm log4j-1.2-api/src/main/java/org/apache/log4j/builders/layout/*Xml*.java
rm log4j-api/src/main/java/org/apache/logging/log4j/util/Activator.java
rm -r log4j-1.2-api/src/main/java/org/apache/log4j/or/jms
%endif

%mvn_alias :%{name}-1.2-api %{name}:%{name}

# Note that packages using the compatibility layer still need to have log4j-core
# on the classpath to run. This is there to prevent build-classpath from putting
# whole dir on the classpath which results in loading incorrect provider
%mvn_file ':{%{name}-1.2-api}' %{name}/@1 %{name}

%mvn_package ':%{name}-slf4j-impl' slf4j
%mvn_package ':%{name}-to-slf4j' slf4j
%mvn_package ':%{name}-taglib' taglib
%mvn_package ':%{name}-jcl' jcl
%mvn_package ':%{name}-jmx-gui' jmx-gui
%mvn_package ':%{name}-web' web
%mvn_package ':%{name}-bom' bom
%mvn_package ':%{name}-cassandra' nosql
%mvn_package ':%{name}-couchdb' nosql

%mvn_package :log4j-core-its __noinstall

%mvn_package ::zip: __noinstall

%pom_remove_dep com.sun.mail:javax.mail log4j-core
%pom_remove_dep javax.mail:javax.mail-api log4j-core
%pom_remove_dep javax.activation:javax.activation-api log4j-core
rm log4j-core/src/main/java/org/apache/logging/log4j/core/net/MimeMessageBuilder.java
rm log4j-core/src/main/java/org/apache/logging/log4j/core/net/SmtpManager.java
rm log4j-core/src/main/java/org/apache/logging/log4j/core/appender/SmtpAppender.java
rm log4j-core/src/main/java/org/apache/logging/log4j/core/filter/MutableThreadContextMapFilter.java

%pom_remove_dep org.eclipse.angus:angus-activation log4j-jakarta-smtp
%pom_remove_dep org.eclipse.angus:jakarta.mail log4j-jakarta-smtp

%pom_remove_plugin -r org.apache.maven.plugins:maven-failsafe-plugin
%pom_remove_plugin -r org.ops4j.pax.exam:exam-maven-plugin

%build
# missing test deps (mockejb)
%mvn_build -j -f

%install
%mvn_install

%if %{without jp_minimal}
%jpackage_script org.apache.logging.log4j.jmx.gui.ClientGUI '' '' %{name}/%{name}-jmx-gui:%{name}/%{name}-core %{name}-jmx false
%endif

%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%files slf4j -f .mfiles-slf4j
%files jcl -f .mfiles-jcl
%files web -f .mfiles-web
%files bom -f .mfiles-bom
%if %{without jp_minimal}
%files taglib -f .mfiles-taglib
%files nosql -f .mfiles-nosql
%files jmx-gui -f .mfiles-jmx-gui
%{_bindir}/%{name}-jmx
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.20.0-25
- Latest state for log4j

* Thu Sep 04 2025 Jiri Vanek <jvanek@redhat.com> - 2.20.0-24
- manual bodhi update for jdk25 needed on selected pkgs

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 2.20.0-23
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-21
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-20
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-19
- Switch to javapackages tests from CentOS Stream GitLab

* Thu Mar 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-18
- Drop javadoc package

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-16
- Drop explicit requires on javapackages-tools

* Wed Jul 24 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-9
- Install license files in licensedir instead of docdir

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.20.0-7
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 2.20.0-6
- bump of release for for java-21-openjdk as system jdk

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.20.0-3
- Rebuild

* Tue Aug 22 2023 Marian Koncek <mkoncek@redhat.com> - 2.20.0-2
- Do not install zip files

* Mon Aug 21 2023 Marian Koncek <mkoncek@redhat.com> - 2.20.0-1
- Update to upstream version 2.20.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 17 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.17.2-9
- Re-enable javadoc package

* Fri Feb 24 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.17.2-8
- Remove dependency on jackson in jp_minimal mode

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Marian Koncek <mkoncek@redhat.com> - 2.17.2-6
- Re-add log4j-web subpackage

* Thu Oct 13 2022 Marian Koncek <mkoncek@redhat.com> - 2.17.2-5
- Remove the rest of glyphicons files

* Thu Oct 13 2022 Marian Koncek <mkoncek@redhat.com> - 2.17.2-4
- Remove glyphicons zip archive from source package

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 26 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.17.2-2
- Fix compatibility with Java 8

* Sun Feb 27 2022 Paul Wouters <paul.wouters@aiven.io> - 2.17.2-1
- Resolves: rhbz#2058949 log4j-2.17.2 is available (1.2 bridge bugfixes)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.17.1-4
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Malcolm Inglis <miinglis@amazon.com> - 2.17.1-2
- Enable GPG signature verification of sources

* Tue Dec 28 2021 Paul Wouters <paul.wouters@aiven.io> - 2.17.1-1
- Update log4j to 2.17.1 for CVE-2021-44832 RCE via JDBC Appender (when attacker controls config)

* Sat Dec 18 2021 Paul Wouters <paul.wouters@aiven.io> - 2.17.0-1
- Update log4j to 2.17.0 for CVE-2021-45105 Denial of Service attack

* Mon Dec 13 2021 Paul Wouters <paul.wouters@aiven.io> - 2.16.0-1
- Update log4j to 2.16.0 - Disables JNDI by default

* Sun Dec 12 2021 Sérgio Basto <sergio@serjux.com> - 2.15.0-1
- Update log4j to 2.15.0 (#2030907)
- Security fix for CVE-2021-44228 (#2030945)

* Sun Aug 01 2021 Sérgio Basto <sergio@serjux.com> - 2.14.1-1
- Update to 2.14.1
- Disable javadoc (#1988896)
- Build with jansi-2
- Remove deps on slf4j-ext (no longer available in Fedora 35)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 2.13.3-2
- Update jansi dep to jansi1

* Thu Aug 20 2020 Fabio Valentini <decathorpe@gmail.com> - 2.13.3-1
- Update to version 2.13.3.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Fabio Valentini <decathorpe@gmail.com> - 2.13.1-3
- Add missing javax.activation dependency.

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.13.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Mar 02 2020 Fabio Valentini <decathorpe@gmail.com> - 2.13.1-1
- Update to version 2.13.1.
- Drop upstream patch that's included in the new release.
- Rebase patch for removing the unsupported SLF4J EventDataConverter.

* Thu Jan 30 2020 Fabio Valentini <decathorpe@gmail.com> - 2.13.0-3
- Add upstream patch for compatibility with the latest slf4j versions.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Alexander Scheel <ascheel@redhat.com> - 2.13.0-1
- Rebase to version 2.13.0

* Sun Oct 20 2019 Fabio Valentini <decathorpe@gmail.com> - 2.12.1-1
- Update to version 2.12.1.

* Mon Sep 30 2019 Fabio Valentini <decathorpe@gmail.com> - 2.12.0-1
- Update to version 2.12.0.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Miro Hrončok <mhroncok@redhat.com> - 2.11.1-4
- Drop log4j-taglib, log4j-web, log4j-bom, log4j-nosql and log4j-jmx-gui

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 2.11.1-2
- Add explicit requirement on javapackages-tools for log4j-jmx
  script. See RHBZ#1600426.

* Tue Aug 07 2018 Michael Simacek <msimacek@redhat.com> - 2.11.1-1
- Update to upstream version 2.11.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Michael Simacek <msimacek@redhat.com> - 2.9.1-4
- Disable liquibase to fix FTBFS

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 13 2017 Michael Simacek <msimacek@redhat.com> - 2.9.1-2
- Update to upstream version 2.9.1

* Mon Sep 18 2017 Michael Simacek <msimacek@redhat.com> - 2.9.0-1
- Update to upstream version 2.9.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 Michael Simacek <msimacek@redhat.com> - 2.8.2-1
- Update to upstream version 2.8.2

* Wed Mar 29 2017 Michael Simacek <msimacek@redhat.com> - 2.8.1-1
- Update to upstream version 2.8.1

* Wed Mar 15 2017 Michael Simacek <msimacek@redhat.com> - 2.7-4
- Add jp_minimal conditional

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 2.7-2
- Cleanup osgi parts
- Add conditional for nosql

* Wed Nov 09 2016 Michael Simacek <msimacek@redhat.com> - 2.7-1
- Update to upstream version 2.7
- Remove stuff marked as "Remove in F24"

* Thu Jun 23 2016 Michael Simacek <msimacek@redhat.com> - 2.6.1-1
- Update to upstream version 2.6.1

* Thu Jun 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5-4
- Remove RAT depenency from BOM package

* Mon May 23 2016 Michael Simacek <msimacek@redhat.com> - 2.5-3
- Remove maven-remote-resources-plugin to fix FTBFS

* Mon Feb 15 2016 Michael Simacek <msimacek@redhat.com> - 2.5-2
- Split log4j-liquibase into separate subpackage

* Mon Feb 15 2016 Michael Simacek <msimacek@redhat.com> - 2.5-1
- Update to upstream version 2.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3-1
- Update to upstream version 2.3

* Thu Feb 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-1
- Update to upstream version 2.2

* Mon Jan 19 2015 Michael Simacek <msimacek@redhat.com> - 2.0-2
- Remove site-plugin from all poms

* Fri Jul 18 2014 Michael Simacek <msimacek@redhat.com> 2.0-1
- Update to upstream version 2.0
- Remove osgi subpackage (osgi parts were moved to corresponding artifacts)
- Add web, bom, nosql subpackages (new)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0-0.2.rc1
- Drop provides for log4j-manual

* Fri May 09 2014 Michael Simacek <msimacek@redhat.com> - 0:2.0-0.1.rc1
- Update to upstream version 2.0-rc1
- Split into subpackages
- Remove logfactor and chainsaw scripts which are no longer shipped
- Remove XML catalogs which are no longer shipped

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.17-16
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 0:1.2.17-15
- Set javamail and geronimo-jms dependency scopes to provided (removes requires)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Michal Srb <msrb@redhat.com> - 0:1.2.17-13
- Enable tests
- Fix BR

* Tue May 14 2013 Ville Skyttä <ville.skytta@iki.fi> - 0:1.2.17-12
- Add DTD public id to XML and SGML catalogs.

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-11
- Remove unneeded BR: maven-idea-plugin

* Thu Apr 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-10
- Fix manpage names, thanks to Michal Srb for reporting

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-9
- Reindex sources in more sensible way
- Add manual pages; resolves: rhbz#949413

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.2.17-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-6
- Build aggregated javadocs with xmvn

* Fri Jan 18 2013 Michal Srb <msrb@redhat.com> - 0:1.2.17-5
- Build with xmvn

* Mon Sep 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.17-4
- Generate javadocs without maven skin

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.17-2
- Remove "uses" OSGI directives from MANIFEST (related #826776)

* Mon Jun 04 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.17-1
- Update to latest version
- Change OSGI bundle symbolic name to org.apache.log4j
- Resolves #826776

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.16-10
- Remove duplicate import-package declaration.
- Adapt to current guidelines.
- Remove no longer needed patches.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Ville Skyttä <ville.skytta@iki.fi> - 0:1.2.16-8
- Drop executable file mode bits from icons.

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-7
- Use package instead of install mvn target to fix build

* Thu Dec 16 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.16-6
- Do not require jaxp_parser_impl. Maven build is not using it all and it's provided by every Java5 JVM.

* Thu Dec  9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-5
- Add patch to fix ant groupId
- Versionless jars & javadocs

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-4
- Fix BRs to include ant-junit
- Fix changed path for javadocs after build run

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-3
- Add license to javadoc and manual subpackages

* Fri May 28 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-2
- Install pom file
- Trim changelog
- Add jpackage-utils to javadoc Requires

* Mon May 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.16-1
- Complete re-working of whole ebuild to work with maven
- Rebase to new version
- Drop gcj support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.14-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.14-5.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.14-4.3
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.14-4jpp.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.14-4jpp.1
- Autorebuild for GCC 4.3

* Sat May 26 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.2.14-3jpp.1
- Upgrade to 1.2.14
- Modify the categories for the .desktop files so they are only
  displayed under the development/programming menus
- Resolves: bug 241447

* Fri May 11 2007 Jason Corley <jason.corley@gmail.com> 0:1.2.14-3jpp
- rebuild through mock and centos 4
- replace vendor and distribution with macros

* Fri Apr 20 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.14-2jpp
- Patch to allow build of org.apache.log4j.jmx.* with mx4j
- Restore Vendor: and Distribution:

* Sat Feb 17 2007 Fernando Nasser <fnasser@redhat.com> - 0:1.2.14-1jpp
- Upgrade

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.13-4jpp
- Add bootstrap option to build core

* Wed Aug 09 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-3jpp.2
- Remove patch for BZ #157585 because it doesnt seem to be needed anymore.

* Tue Aug 08 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-3jpp.1
- Re-sync with latest from JPP.
- Update patch for BZ #157585 to apply cleanly.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.2.13-2jpp_2fc
- Rebuilt

* Fri Jul 21 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:1.2.13-2jpp_1fc
- Merge spec and patches with latest from JPP.
- Clean source tar ball off prebuilt jars and classes.
- Use classpathx-jaf and jms for buildrequires for the time being.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.2.8-7jpp_9fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.2.8-7jpp_8fc
- fix scriptlet spew

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:1.2.8-7jpp7fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov  3 2005 Archit Shah <ashah@redhat.com> 0:1.2.8-7jpp_6fc
- Reenable building of example that uses rmic

* Wed Jun 22 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_5fc
- Reenable building of classes that require jms.
- Remove classes and jarfiles from the tarball.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_4fc
- Work around chainsaw failure (#157585).

* Tue Jan 11 2005 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_3fc
- Reenable building of classes that require javax.swing (#130006).

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:1.2.8-7jpp_2fc
- Build into Fedora.

## END: Generated by rpmautospec
