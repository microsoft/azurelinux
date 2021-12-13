Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package avalon-logkit
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2000-2005, JPackage Project
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define     short_name      logkit
%define     camelcase_short_name      LogKit
Name:           avalon-logkit
Version:        2.1
Release:        23%{?dist}
Summary:        Java logging toolkit
License:        Apache-2.0
Group:          Development/Libraries/Java
Url:            http://avalon.apache.org/%{short_name}/
#Source0:       http://www.apache.org/dist/excalibur/%{name}/source/%{name}-%{version}-src.zip
#Source1:       http://repo1.maven.org/maven2/avalon-logkit/avalon-logkit/%{version}/%{name}-%{version}.pom
Source0:        %{name}-%{version}-src.zip
Source1:        %{name}-%{version}.pom
Patch0:         fix-java6-compile.patch
Patch1:         avalon-logkit-pom-deps.patch
Patch2:         avalon-logkit-encoding.patch
Patch3:         fix-java7-compile.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  geronimo-jms-1_1-api
BuildRequires:  glassfish-servlet-api
BuildRequires:  java-devel >= 1.8
BuildRequires:  javamail
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  log4j12
BuildRequires:  unzip
Requires:       mvn(javax.jms:jms)
Requires:       mvn(javax.mail:mail)
Requires:       mvn(javax.servlet:servlet-api)
BuildArch:      noarch

%description
LogKit is a logging toolkit designed for secure performance oriented
logging in applications. To get started using LogKit, it is recomended
that you read the whitepaper and browse the API docs.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0
cp %{SOURCE1} pom.xml
%patch1
%patch2 -p1
%patch3

# remove all binary libs
find . -name "*.jar" -delete

%build
ant clean
mkdir -p target/lib
build-jar-repository -s -p target/lib \
                   log4j12/log4j-12 \
                   javamail/mailapi \
                   geronimo-jms-1.1-api \
                   glassfish-servlet-api

ant -Dant.build.javac.source=8 -Dant.build.javac.target=8 \
    -Dencoding=ISO-8859-1 -Dnoget=true -lib %{_datadir}/java \
    jar javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

#pom
install -d -m 755 %{buildroot}/%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "%{short_name}:%{short_name},org.apache.avalon.logkit:%{name}"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_datadir}/maven-metadata/%{name}.xml
%{_mavenpomdir}/JPP-%{name}.pom

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-23
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1-22.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Remove dependency on jdbc-stdext.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against compatibility log4j12 package
* Mon Apr 15 2019 Fridrich Strba <fstrba@suse.com>
- Depend directly on the geronimo-jms-1_1-api package instead of
  the jms virtual provider
* Thu Feb 14 2019 Fridrich Strba <fstrba@suse.com>
- Build against the glassfish-servlet-api
* Tue Jan 22 2019 Fridrich Strba <fstrba@suse.com>
- Require dependencies by their maven artifactId and groupId in
  order to be usable from maven build
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Fri Sep 15 2017 jengelh@inai.de
- RPM group and minor spelling fix. Replacement of
  - exec rm by -delete.
* Fri Sep 15 2017 fstrba@suse.com
- Fix build with jdk9 by specifying java source and target 1.6
- Clean spec file
* Sun May 21 2017 tchvatal@suse.com
- Remove unneeded dependencies
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
* Thu Jun  4 2015 dimstar@opensuse.org
- Also adjust Requires to be servlet >= 3.0 instead of servlet30.
* Thu Jun  4 2015 dimstar@opensuse.org
- BuildRequire servlet >= 3.0 instead of 'servlet30'. Since tomcat
  moved to version 8.0, it now provides 'servlet31' (which is fine,
  as this is represented as servlet 3.1).
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Jun 27 2014 tchvatal@suse.com
- Cleanup with spec-cleaner
- Build on SLE11
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Jun 20 2012 mvyskocil@suse.cz
- bump servletapi to 30 (tomcat7)
* Fri May 18 2012 mvyskocil@suse.cz
- add pom file
- fix a build with openjdk7
- change the jms to jms_api in classpath
* Thu Feb 16 2012 cfarrell@suse.com
- license update: Apache-2.0
  Look at License.txt
* Sun Dec 18 2011 nlminhtl@gmail.com
- Package avalon-logkit 2.1 for openSUSE
- Fixing the license for openSUSE
