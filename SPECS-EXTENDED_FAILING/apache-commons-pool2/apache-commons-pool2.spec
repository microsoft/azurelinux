Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-pool2
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define base_name       pool
%define short_name      commons-%{base_name}2
Name:           apache-commons-pool2
Version:        2.4.2
Release:        6%{?dist}
Summary:        Apache Commons Pool 2.x series
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-pool/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         jakarta-commons-pool-build.patch
BuildRequires:  ant
BuildRequires:  cglib
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
Requires:       cglib
Provides:       %{short_name} = %{version}
Obsoletes:      %{short_name} < %{version}
BuildArch:      noarch

%description
The goal of the Pool 2.x package is to create and maintain an object
(instance) pooling package to be distributed under the ASF license. The
package supports a variety of pool implementations, but encourages
support of an interface that makes these implementations
interchangeable.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
The goal of Pool 2.x package it to create and maintain an object (instance)
pooling package to be distributed under the ASF license. The package
should support a variety of pool implementations, but encourage support
of an interface that makes these implementations interchangeable.

This package contains the javadoc documentation for the Apache Commons
Pool 2.x Package.

%prep
%setup -q -n %{short_name}-%{version}-src
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%patch0

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.apache.commons</groupId>" .

%build
echo "cglib.jar=$(build-classpath cglib)" >> build.properties
ant \
    -Djavac.target.version=8 -Djavac.src.version=8 \
    -Djava.io.tmpdir=. clean dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files
%license LICENSE.txt
%doc README.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{short_name}.jar
%{_javadir}/%{short_name}-%{version}.jar
%{_mavenpomdir}/%{name}-%{version}.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.2-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.4.2-5.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Thu Sep 14 2017 fstrba@suse.com
- Fix javadoc build
* Thu Sep 29 2016 tchvatal@suse.com
- Version update to 2.4.2 release from pool2:
  * rename to latest 2.x pool series for dbcp and other packages
* Thu Sep 29 2016 tchvatal@suse.com
- Rename from jakarta-commons-pool to apache-commons-pool
- Version update to 1.6:
  * drop the tomcat5 package, we need pool2 to work with new tomcat
  * Last and final from the pool1 series, new pool2 was introduced
    for future developement.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Mar 13 2008 mvyskocil@suse.cz
- merged with jpackage 1.7
- update to 1.3
- changes in BuildRequires:
  - java2-deve-packages was substituded by java-devel
  - added a junit
  - added a maven build support and maven related BuildRequires
  - xml-commons-apis was moved to the maven build branch
- added a gcj build support
- included a maven depmap files
- remove a source=1.4 from build and a java14compat patch
- provides and obsoletes of main package contains the version
- new tomcat5 subpackage
- new manual subpackage (build only with maven)
* Fri Sep 15 2006 ro@suse.de
- set source=1.4 for java
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jul 28 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.2 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.2 (JPackage 1.5)
