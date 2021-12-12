Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-dbcp
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


%define base_name       dbcp
%define short_name      commons-%{base_name}2
Name:           apache-commons-dbcp
Version:        2.1.1
Release:        7%{?dist}
Summary:        Jakarta Commons DataBase Pooling Package
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-dbcp/
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source100:      http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz.asc
Source101:      commons.keyring
Patch0:         apache-commons-dbcp-sourcetarget.patch
Patch1:         apache-commons-dbcp-javadoc.patch
BuildRequires:  ant >= 1.6.5
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-pool2
BuildRequires:  fdupes
BuildRequires:  geronimo-jta-1_1-api
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit >= 3.8.1
BuildRequires:  xerces-j2
Requires:       commons-collections >= 3.2
Requires:       commons-pool2
Requires:       jta_api >= 1.1
Requires(post): update-alternatives
Requires(preun): update-alternatives
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       hibernate_jdbc_cache
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The DBCP package creates and maintains a database connection pool
package written in the Java language to be distributed under the ASF
license. The package is available as a pseudo-JDBC driver and via a
DataSource interface. The package also supports multiple logins to
multiple database systems, reclamation of stale or dead connections,
testing for valid connections, PreparedStatement pooling, and other
features.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
This package contains the javadoc documentation for the DBCP package.

The DBCP package shall create and maintain a database connection pool
package written in the Java language to be distributed under the ASF
license. The package shall be available as a pseudo-JDBC driver and via
a DataSource interface. The package shall also support multiple logins
to multiple database systems, reclamation of stale or dead connections,
testing for valid connections, PreparedStatement pooling, and other
features.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1
%patch1 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%pom_remove_parent .

%build
ant \
        -Dcommons-pool.jar=$(build-classpath commons-pool2) \
        -Djdbc20ext.jar=$(build-classpath jdbc-stdext) \
        -Djunit.jar=$(build-classpath junit) \
        -Dxerces.jar=$(build-classpath xerces-j2) \
        -Dxml-apis.jar=$(build-classpath xml-commons-jaxp-1.3-apis) \
        -Dcommons-logging.jar=$(build-classpath commons-logging) \
        -Djava.io.tmpdir=. \
        -Djta-impl.jar=$(build-classpath geronimo-jta-1.1-api) \
        dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}2-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}2-%{version}.pom
%add_maven_depmap %{name}2-%{version}.pom %{name}2-%{version}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}
# hibernate_jdbc_cache ghost symlink
mkdir -p %{buildroot}%{_sysconfdir}/alternatives/
ln -sf %{_sysconfdir}/alternatives/hibernate_jdbc_cache.jar %{buildroot}%{_javadir}/hibernate_jdbc_cache.jar

%post
update-alternatives --install %{_javadir}/hibernate_jdbc_cache.jar \
  hibernate_jdbc_cache %{_javadir}/%{name}2.jar 60

%preun
if [ $1 -eq 0 ] ; then
  update-alternatives --remove hibernate_jdbc_cache %{_javadir}/%{name}2.jar
fi

%files
%license LICENSE.txt
%{_javadir}/%{name}2.jar
%{_javadir}/%{name}2-%{version}.jar
%{_javadir}/%{short_name}.jar
%{_javadir}/%{short_name}-%{version}.jar
%{_javadir}/hibernate_jdbc_cache.jar
%ghost %{_sysconfdir}/alternatives/hibernate_jdbc_cache.jar
%{_mavenpomdir}/%{name}2-%{version}.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.1-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1.1-6.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Remove dependency on jdbc-stdext.

* Mon Apr 15 2019 Fridrich Strba <fstrba@suse.com>
- Build classpath using directly geronimo-jta-1.1-api instead of
  the jta symlink
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Sat Dec 15 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file
* Tue May 15 2018 fstrba@suse.com
- Added patches:
  * apache-commons-dbcp-sourcetarget.patch
    + build with java source / target 8 to align with other
  packages
  * apache-commons-dbcp-javadoc.patch
    + do not attempt to load urls while building
* Mon Oct 31 2016 tchvatal@suse.com
- Search for jta not jta-api as SLE has issues locating the api while
  the jta is just simple symlink
* Thu Sep 29 2016 tchvatal@suse.com
- Update version to 2.1.1 wrt fate#321029
  * Fixes to actually work with tomcat 8
* Thu Sep 29 2016 jmatejek@suse.com
- rename to apache-commons-dbcp
- updating requirements
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Sep 23 2014 tchvatal@suse.com
- Do not require tomcat, it is just test dependency causing cycle
  bnc#954603
* Mon Jul 28 2014 tchvatal@suse.com
- Update the alternatives once more to match docu.
* Mon Jul 21 2014 tchvatal@suse.com
- Fixup the update-alternatives code.
- Get rid of the old maven code that we didn't use
* Fri Jul 11 2014 tchvatal@suse.com
- Cleanup with spec-cleaner
* Tue Nov 26 2013 mvyskocil@suse.com
- Move -src subpackage to extra spec file
* Wed Oct 30 2013 mvyskocil@suse.com
- Create -src subpackage in order to create tomcat-dbcp.jar without
  build cycles (bnc#847505)
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Sep  5 2013 mvyskocil@suse.com
- don't require commons-collections-tomcat5 for build
- drop -tomcat5 subpackage
- use new add_maven_depmap macro
- drop source url as apache stops to distribute such old version
* Wed Jun 20 2012 mvyskocil@suse.cz
- require tomcat-lib for build
* Fri May 25 2012 mvyskocil@suse.cz
- fix build with jdk7
- remove note needed obsolete
- rename tomcat5 subpackage to tomcat
- use non-versioned javadocdir
* Thu Nov  6 2008 ro@suse.de
- add buildignore for jakarta-commons-dbcp-tomcat5
  (workaround for bs bug)
* Thu Aug 28 2008 mvyskocil@suse.cz
- target=1.5 source=1.5
* Thu Jul 31 2008 mvyskocil@suse.cz
- do not add a java6 compatibility for javac 1.5.0 (fixed build on ia64)
* Tue Jul 29 2008 anosek@suse.cz
- made the symlink jakarta-commons-dbcp -> jakarta-commons-dbcp-1.2.2
  part of the javadoc package
* Mon Jul 21 2008 mvyskocil@suse.cz
- merged with jpackage 1.7 spec
  - added a tomcat5 subpackage (to fix [bnc#408253])
  - added a maven build branch (n/a in suse yet):
  - added a poms and project.xmls for maven
  - added a depmagfrags for maven
- build againts tomcat6 (instead of tomcat5 as in original jpackage project)
- add a java6 compatibility patch
* Wed Apr  9 2008 mvyskocil@suse.cz
- update to 1.2.2
- remove the java14compat patch
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Oct 12 2005 jsmeix@suse.de
- Removed jdbc-stdext from build-classpath because it is
  not needed for build.
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.2.1 from JPackage.org
* Fri Sep  3 2004 skh@suse.de
- Initial package created with version 1.2.1 (JPackage 1.5)
