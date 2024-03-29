#
# spec file for package hamcrest
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
	
%global upstream_version %(echo %{version} | tr '~' '-')
%global debug_package %{nil}

Summary:        Library of matchers for building test expressions
Name:           hamcrest
Version:        2.2
Release:        1%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/hamcrest/JavaHamcrest
Source0:        https://github.com/hamcrest/JavaHamcrest/archive/v%{upstream_version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://repo1.maven.org/maven2/org/hamcrest/hamcrest/%{upstream_version}/hamcrest-%{upstream_version}.pom
Patch0:         0001-Fix-build-with-OpenJDK-11.patch

BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven
Provides:       mvn(org.hamcrest:hamcrest-core) 

%description
Provides a library of matcher objects (also known as constraints or
predicates) allowing 'match' rules to be defined declaratively, to be
used in other frameworks. Typical scenarios include testing frameworks,
mocking libraries and UI validation rules.

%package javadoc
Summary:        Javadoc for %{name}
 
%description javadoc
Javadoc for %{name}.
 
%prep
%setup -q -n JavaHamcrest-%{upstream_version}
%patch 0 -p1

sed -i 's/\r//' LICENSE.txt
 
pushd hamcrest
cp -p %{SOURCE1} pom.xml
%pom_add_dep junit:junit::test
%pom_xpath_inject pom:project '
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>any</version>
      <configuration>
        <source>1.8</source>
        <target>1.8</target>
      </configuration>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-jar-plugin</artifactId>
      <version>any</version>
      <configuration>
        <archive>
          <manifestEntries>
            <Automatic-Module-Name>org.hamcrest</Automatic-Module-Name>
          </manifestEntries>
        </archive>
      </configuration>
    </plugin>
  </plugins>
</build>'
 
%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-all
%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-core
%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-library
 
%build
pushd hamcrest
%mvn_build -f
popd
 
%install
pushd hamcrest
%mvn_install
popd
 
%files -f hamcrest/.mfiles
%doc README.md
%license LICENSE.txt
 
%files javadoc -f hamcrest/.mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Feb 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 2.2-1
- upgrade to 2.2 - none

* Mon Apr 3 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.3-16
- Added provides for maven artifacts for core subpackage

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.3-15
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-14
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.3-13.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Wed Oct  2 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to the hamcrest-parent pom and do not
  distribute it
  * useless since we don't build with maven
  * creates problems with gradle connector
* Tue Jan 15 2019 Fridrich Strba <fstrba@suse.com>
- Make jmock and easymock integration opt-in (bsc#1121956)
* Fri Jan  4 2019 Fridrich Strba <fstrba@suse.com>
- Use sources from github, which are accessible
- Do not build the hamcrest-text empty jar
- Split a core package off the main package
- Added patch:
  * hamcrest-1.3-qdox-2.0.patch
    + Fix build against QDox 2.0
- Removed patch:
  * hamcrest-1.3-no-integration.patch
    + Not needed any more since integration is buildable
- Modified patches:
  * hamcrest-1.3-build.patch
  * hamcrest-1.3-fork-javac.patch
  * hamcrest-1.3-javadoc.patch
  * hamcrest-1.3-javadoc10.patch
  * hamcrest-1.3-javadoc9.patch
  * hamcrest-1.3-no-jarjar.patch
  * hamcrest-1.3-random-build-crash.patch
* Mon Dec 18 2017 fstrba@suse.com
- Added patch:
  * hamcrest-1.3-javadoc10.patch
    + Fix build with jdk10's javadoc that ends in error when a
    link cannot be downloaded
* Fri Sep  8 2017 fstrba@suse.com
- Modified patch:
  * hamcrest-1.3-fork-javac.patch
    + Specify java target level 1.6 in order to allow building
    with jdk9
- Specify java source level 1.6 in order to allow building with
  jdk9
- Added patch:
  * hamcrest-1.3-javadoc9.patch
    + fix javadoc errors that are fatal in jdk9
* Mon May 29 2017 tchvatal@suse.com
- Apply patch from fedora:
  * hamcrest-1.3-fork-javac.patch
* Fri May 19 2017 tchvatal@suse.com
- Fix homepage
- Update to build with new javapacakges-tools
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Jul  7 2014 tchvatal@suse.com
- Use junit not junit4
* Mon Jun 16 2014 tchvatal@suse.com
- Add patch to fix random build errors by enforcing single thread.
  * hamcrest-1.3-random-build-crash.patch
* Tue Oct 29 2013 mvyskocil@suse.com
- drop junit from dependencies, it's not needed and cause a build cycle
* Mon Oct 21 2013 mvyskocil@suse.com
- Update to 1.3
  bugfix and feature update, see CHANGES.txt for details
- Removed patches
  * hamcrest-1.1-build.patch
    + renamed to hamcrest-1.3-build.patch
  * hamcrest-1.1-no-jarjar.patch
    + renamed to hamcrest-1.3-no-jarjar.patch
  * hamcrest-1.1-no-integration.patch
    + renamed to hamcrest-1.3-no-integration.patch
- Added patches
  * hamcrest-1.3-javadoc.patch
- Updated poms and added OSGI manifests from Fedora
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Tue Sep  3 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
- install non-versioned dirs and jars
* Tue May  5 2009 mvyskocil@suse.cz
- Initial packaging of 1.1 in SUSE (from jpp 5.0)