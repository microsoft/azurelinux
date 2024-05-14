Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-lang
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2000-2009, JPackage Project
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


%define base_name lang
%define short_name commons-%{base_name}
Name:           apache-commons-lang
Version:        2.6
Release:        17%{?dist}
Summary:        Apache Commons Lang Package
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/%{base_name}
Source0:        https://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         fix_StopWatchTest_for_slow_systems.patch
Patch1:         0002-Fix-FastDateFormat-for-Java-7-behaviour.patch
Patch2:         commons-lang-bundle-manifest.patch
Patch3:         encoding-fix.patch
Patch4:         removing-enum-package.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
# Java 8 is the last version that can build with source and target level 1.4
BuildConflicts: java-devel >= 1.9
BuildConflicts: java-headless >= 1.9
# Avoid building with OpenJ9 on supported platforms; to prevent build cycle
BuildConflicts: java-devel-openj9
BuildConflicts: java-headless-openj9
Provides:       %{short_name} = %{version}-%{release}
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}-%{release}
BuildArch:      noarch

%description
The standard Java libraries fail to provide enough methods for
manipulation of its core classes. The Commons Lang Component provides
these extra methods.

The Commons Lang Component provides a host of helper utilities for the
java.lang API, notably String manipulation methods, basic numerical
methods, object reflection, creation and serialization, and System
properties. Additionally it contains an inheritable enum type, an
exception structure that supports multiple types of nested-Exceptions
and a series of utilities dedicated to help with building methods, such
as hashCode, toString and equals.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch 0
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
sed -i 's/\r//' *.txt *.html

%pom_remove_parent .

%build
export OPT_JAR_LIST=`cat %{_sysconfdir}/ant.d/junit`
export CLASSPATH=
%{ant} \
    -Dcompile.source=1.6 -Dcompile.target=1.6 \
    -Djunit.jar=$(build-classpath junit4) \
    -Dfinal.name=%{short_name} \
    -Djdk.javadoc=%{_javadocdir}/java \
    jar javadoc

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p target/%{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && for jar in apache-*; do ln -sf ${jar} `echo $jar| sed "s|apache-||g"`; done)

# pom
mkdir -p %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr target/apidocs/* %{buildroot}%{_javadocdir}/%{name}/

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc PROPOSAL.html RELEASE-NOTES.txt
%{_javadir}/%{short_name}.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Fri Feb 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-17
- Using newer Java version to fix build.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-16
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.6-15.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Mon Mar 23 2020 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * commons-lang-bundle-manifest.patch
    + Add bundle manifest to make usable from eclipse
* Mon Jan 27 2020 Fridrich Strba <fstrba@suse.com>
- On supported platforms, avoid building with OpenJ9 in order to
  prevent a build cycle.
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Mon Feb  4 2019 Fridrich Strba <fstrba@suse.com>
- Clean up the spec file
* Tue Mar 20 2018 marco.strigl@suse.com
- fix flaky StopWatch tests on slow systems by increasing the max value (bsc#1085999)
  * fix_StopWatchTest_for_slow_systems.patch
* Mon Oct  2 2017 fstrba@suse.com
- Require java-devel < 1.9 because all those versions can use
  target level < 1.5
* Sun Sep 10 2017 fstrba@suse.com
- Require for build java-devel = 1.8.0, since it is the last
  version being able to build with source and target levels < 1.5
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4
* Fri Sep  6 2013 mvyskocil@suse.com
- update to 2.6 (bugfix release)
  * see https://commons.apache.org/proper/commons-lang/release-notes/RELEASE-NOTES-2.6.txt
  * see https://commons.apache.org/proper/commons-lang/release-notes/RELEASE-NOTES-2.5.txt
- use new add_maven_depmap macro
- drop jakarta-commons-lang-build.patch
* Wed Jan 27 2010 mvyskocil@suse.cz
- merged with jakarta-commons-lang-2.1-7.jpp5.src.rpm
* Tue Jul 29 2008 anosek@suse.cz
- made the symlink jakarta-commons-lang -> jakarta-commons-lang-2.3
  part of the javadoc package
* Mon Jul 21 2008 mvyskocil@suse.cz
- update to 2.3
  - merged with japackage 1.7 spec file
  - add a maven build support and a maven pom files and post/un scripts for
  depmap files
- removed a source=1.1 - fixed build under openjdk6
- removed a crosslink patch
* Fri Sep 15 2006 ro@suse.de
- use source=1.1 for java
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Aug 29 2005 jsmeix@suse.de
- Removed the "test" to be built so that it builds now on all
  architectures (see bug 102629).
  The "test" failed on ppc, s390x, and ppc64 (see bug 113779).
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 2.0 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.0 (JPackage 1.5)
