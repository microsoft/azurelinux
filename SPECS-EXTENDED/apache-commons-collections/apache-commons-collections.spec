Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-collections
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


%define base_name       collections
%define short_name      commons-%{base_name}
Name:           apache-commons-collections
Version:        3.2.2
Release:        7%{?dist}
Summary:        Commons Collections Package
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-collections
Source0:        https://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        commons-collections-testframework.pom
Patch0:         jakarta-commons-collections-javadoc-nonet.patch
Patch1:         commons-collections-3.2-build_xml.patch
# PATCH-FIX-UPSTREAM build with jdk8
Patch2:         java8-compat.patch
# PATCH-FIX-UPSTREAM add missing MANIFEST.MF file
Patch3:         commons-collections-missing-MF.patch
Patch4:         commons-collections-3.2.2-tf.javadoc.patch
Patch5:         commons-collections-jdk11.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The introduction of the Collections API by Sun in JDK 1.2
has been a boon to quick and effective Java programming.
Ready access to powerful data structures has accelerated
development by reducing the need for custom container
classes around each core object.  Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections
Component strives to fulfill them. Among the features of
this package are: - special-purpose implementations of
Lists and Maps for fast access

- adapter classes from Java1-style containers (arrays,
  enumerations) to Java2-style collections

- methods to test or create typical set theory properties
  of collections such as union, intersection, and closure

%package testframework
Summary:        Test framework for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML
Provides:       %{name}-testframework-javadoc = %{version}-%{release}
Obsoletes:      %{name}-testframework-javadoc < %{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
# remove all binary libs
find . -name "*.jar" -delete
find . -name "*.class" -delete
# Fix file eof
sed -i 's/\r//' LICENSE.txt PROPOSAL.html README.txt NOTICE.txt

%patch 0 -p1
%patch 1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
%patch 5 -p1

# Substitute version into testframework pom
cp -p %{SOURCE1} pom-testframework.xml
sed -i 's/@VERSION@/%{version}/' pom-testframework.xml

%pom_remove_parent .

%build
echo "junit.jar=$(build-classpath junit)" >>build.properties
ant \
    -Dant.build.javac.source=8 -Dant.build.javac.target=8 \
    -Dant.build.javadoc.source=8 -Dtf.build.docs=build/docs/apidocs/ \
    -Djava.io.tmpdir=. jar javadoc tf.validate tf.jar dist.bin dist.src tf.javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 build/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -m 644 build/%{short_name}-testframework-%{version}.jar %{buildroot}%{_javadir}/%{name}-testframework.jar
(cd %{buildroot}%{_javadir} && for jar in *; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
install -Dpm 644 pom-testframework.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}-testframework.pom
%add_maven_depmap JPP-%{short_name}.pom %{short_name}.jar -a "org.apache.commons:%{short_name}"
%add_maven_depmap JPP-%{short_name}-testframework.pom %{short_name}-testframework.jar -f "testframework" -a "org.apache.commons:%{short_name}-testframework"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc PROPOSAL.html README.txt RELEASE-NOTES.txt
%{_javadir}/%{name}.jar

%files testframework -f .mfiles-testframework
%{_javadir}/%{name}-testframework.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.2-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.2.2-6.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Tue Jul 10 2018 fstrba@suse.com
- Added patch:
  * commons-collections-jdk11.patch
    + resolve ambiguity with toArray(null)
  + fixes tests with jdk11
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Fri Sep 29 2017 fstrba@suse.com
- Don't condition the maven defines on release version, but on
  _maven_repository being defined
* Thu Sep 14 2017 fstrba@suse.com
- Fix build with jdk9 by specifying java source and target 1.6
- Added patch:
  * commons-collections-3.2.2-tf.javadoc.patch
  - Fix unresolved symbols when building tf.javadoc
* Fri May 19 2017 tchvatal@suse.com
- Fix build with new javapackages-tools
* Thu Dec 17 2015 tchvatal@suse.com
- Version update to 3.2.2:
  * Various bugfixes
  * Unix formating in the archive
  * Fixes bnc#954102
- Refresh patches for the dos2unix conversion:
  * commons-collections-3.2-build_xml.patch
  * jakarta-commons-collections-javadoc-nonet.patch
- Add patch to add missing MANIFEST.MF file:
  * commons-collections-missing-MF.patch
* Wed Jul 29 2015 tchvatal@suse.com
- Fix build with jdk8:
  * java8-compat.patch
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Jul  7 2014 tchvatal@suse.com
- Do not depend on junit4 but use junit
* Thu May 15 2014 darin@darins.net
- no bytecode check from sles
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Sep  5 2013 mvyskocil@suse.com
- update to 3.2.1
- rename to apache-commons-collections
- deleted patches
  * jakarta-commons-collections-navigation.patch
  * jakarta-commons-collections-target15.patch
- added patches
  * commons-collections-3.2-build_xml.patch
- use newest add_maven_depmap from javapackages-tools
- drop -tomcat5 subpackage
* Tue Nov 11 2008 mvyskocil@suse.cz
- fix of bnc#441085: yast2-schema is missing on media (openSUSE-11. 1-DVD-ppc-Build0113)
  - unittest disabled as it fails on ppc with openjdk b11
* Mon Aug 25 2008 mvyskocil@suse.cz
- target=1.5 source=1.5
* Thu Mar 13 2008 mvyskocil@suse.cz
- merged with jpackage-1.7
- update to 3.2
- changes in BuildRequires:
  - java2-devel-packages was substituded by java-devel
  - added ant-junit
  - maven build support and a maven specific BuildRequires
- added maven pom files
- provides and obsoletes contains a version
- the gcj build support
- new subpackages:
  - jakarta-commons-collections-testframework
  - jakarta-commons-collections-testframework-javadoc
  - jakarta-commons-collections-tomcat5
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 3.1 from JPackage.org
* Mon Feb 21 2005 skh@suse.de
- update to version 3.1
- don't use icecream
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.1.1 (JPackage 1.5)
