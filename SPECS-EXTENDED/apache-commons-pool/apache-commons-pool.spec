%define base_name       pool
%define short_name      commons-%{base_name}
Summary:        Apache Commons Pool
Name:           apache-commons-pool
Version:        1.6
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-pool/
Source0:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         jakarta-commons-pool-build.patch
Patch1:         commons-pool-1.6-sourcetarget.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The goal of the Pool package is to create and maintain an object
(instance) pooling package to be distributed under the ASF license. The
package supports a variety of pool implementations, but encourages
support of an interface that makes these implementations
interchangeable.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
The goal of Pool package it to create and maintain an object (instance)
pooling package to be distributed under the ASF license. The package
should support a variety of pool implementations, but encourage support
of an interface that makes these implementations interchangeable.

This package contains the javadoc documentation for the Apache Commons
Pool Package.

%prep
%setup -q -n %{short_name}-%{version}-src
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
%patch 0
%patch 1 -p1

dos2unix README.txt

%pom_remove_parent .

%build
ant -Djava.io.tmpdir=. clean dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{short_name}-%{version}-SNAPSHOT.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
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

%check
ant -Djava.io.tmpdir=. test

%files
%defattr(0644,root,root,0755)
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
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}

%changelog
* Mon Nov 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.6-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Enable check section
- License verified

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with maven

* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Install as maven artifact

* Tue May 15 2018 fstrba@suse.com
- Modified patch:
  * commons-pool-1.6-sourcetarget.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
- Run fdupes on the documentation

* Thu Sep 14 2017 fstrba@suse.com
- Added patch:
  * commons-pool-1.6-sourcetarget.patch
    + Specify java source and target level 1.6 in order to allow
    building with jdk9

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
