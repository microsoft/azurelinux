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

%bcond_with jmock
%bcond_with easymock

Summary:        Library of matchers for building test expressions
Name:           hamcrest
Version:        1.3
Release:        16%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/hamcrest/JavaHamcrest
Source0:        https://github.com/hamcrest/JavaHamcrest/archive/hamcrest-java-%{version}.tar.gz
Source1:        hamcrest-core-MANIFEST.MF
Source2:        hamcrest-library-MANIFEST.MF
Source3:        hamcrest-integration-MANIFEST.MF
Source4:        hamcrest-generator-MANIFEST.MF
Patch0:         %{name}-%{version}-build.patch
Patch1:         %{name}-%{version}-no-jarjar.patch
Patch3:         %{name}-%{version}-javadoc.patch
Patch4:         %{name}-%{version}-qdox-2.0.patch
Patch5:         %{name}-%{version}-fork-javac.patch
Patch6:         %{name}-%{version}-javadoc9.patch
Patch7:         %{name}-%{version}-javadoc10.patch
Patch8:         %{name}-%{version}-random-build-crash.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  qdox >= 2.0
Requires:       %{name}-core = %{version}-%{release}
Requires:       qdox >= 2.0
BuildArch:      noarch
%if %{with jmock}
BuildRequires:  jmock
Requires:       jmock
%endif
%if %{with easymock}
BuildRequires:  easymock
Requires:       easymock
%endif

%description
Provides a library of matcher objects (also known as constraints or
predicates) allowing 'match' rules to be defined declaratively, to be
used in other frameworks. Typical scenarios include testing frameworks,
mocking libraries and UI validation rules.

%package core
Summary:        Core API of hamcrest matcher framework.
Group:          Development/Libraries/Java
Provides:       mvn(org.hamcrest:hamcrest-core) = %{version}-%{release}

%description core
The core API of hamcrest matcher framework to be used by third-party framework providers.
This includes the a foundation set of matcher implementations for common operations.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demo files for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}
Requires:       junit

%description demo
Demo files for %{name}.

%prep
%setup -q -n JavaHamcrest-%{name}-java-%{version}

find . -type f -name "*.jar" | xargs -t rm
ln -sf $(build-classpath qdox) lib/generator/
%if %{with jmock}
ln -sf $(build-classpath jmock) lib/integration/
%else
rm -fr hamcrest-integration/src/main/java/org/hamcrest/integration/JMock1Adapter.java
rm -fr hamcrest-integration/src/main/java/org/hamcrest/JMock1Matchers.java
rm -fr hamcrest-unit-test/src/main/java/org/hamcrest/integration/JMock1AdapterTest.java
%endif
%if %{with easymock}
ln -sf $(build-classpath easymock3) lib/integration/
%else
rm -fr hamcrest-integration/src/main/java/org/hamcrest/integration/EasyMock2Adapter.java
rm -fr hamcrest-integration/src/main/java/org/hamcrest/EasyMock2Matchers.java
%endif

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

sed -i 's/\r//' LICENSE.txt

%build
export CLASSPATH=$(build-classpath qdox)
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 -Dversion=%{version} -Dbuild.sysclasspath=last clean core generator library bigjar javadoc

# inject OSGi manifests
jar ufm build/%{name}-core-%{version}.jar %{SOURCE1}
jar ufm build/%{name}-library-%{version}.jar %{SOURCE2}
jar ufm build/%{name}-integration-%{version}.jar %{SOURCE3}
jar ufm build/%{name}-generator-%{version}.jar %{SOURCE4}

%install
sed -i 's/@VERSION@/%{version}/g' pom/*.pom

# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}/%{name}

rm -f pom/%{name}-parent.pom
for i in pom/%{name}*.pom; do
  %pom_remove_parent ${i}
  %pom_xpath_inject "pom:project" "
  <groupId>org.hamcrest</groupId>
  <version>%{version}</version>" ${i}
done

install -m 644 build/%{name}-core-%{version}.jar %{buildroot}%{_javadir}/%{name}/core.jar
install -m 644 pom/%{name}-core.pom %{buildroot}%{_mavenpomdir}/%{name}/core.pom
%add_maven_depmap %{name}/core.pom %{name}/core.jar -f core

install -m 644 build/%{name}-all-%{version}.jar %{buildroot}%{_javadir}/%{name}/all.jar
install -m 644 pom/%{name}-all.pom %{buildroot}%{_mavenpomdir}/%{name}/all.pom
%add_maven_depmap %{name}/all.pom %{name}/all.jar

install -m 644 build/%{name}-generator-%{version}.jar %{buildroot}%{_javadir}/%{name}/generator.jar
install -m 644 pom/%{name}-generator.pom %{buildroot}%{_mavenpomdir}/%{name}/generator.pom
%add_maven_depmap %{name}/generator.pom %{name}/generator.jar

install -m 644 build/%{name}-integration-%{version}.jar %{buildroot}%{_javadir}/%{name}/integration.jar
install -m 644 pom/%{name}-integration.pom %{buildroot}%{_mavenpomdir}/%{name}/integration.pom
%add_maven_depmap %{name}/integration.pom %{name}/integration.jar

install -m 644 build/%{name}-library-%{version}.jar %{buildroot}%{_javadir}/%{name}/library.jar
install -m 644 pom/%{name}-library.pom %{buildroot}%{_mavenpomdir}/%{name}/library.pom
%add_maven_depmap %{name}/library.pom %{name}/library.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/temp/hamcrest-all-%{version}-javadoc.jar.contents/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr %{name}-examples %{buildroot}%{_datadir}/%{name}/

%files -f .mfiles
%defattr(0644,root,root,0755)
%license LICENSE.txt

%files core -f .mfiles-core
%defattr(0644,root,root,0755)
%license LICENSE.txt

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%changelog
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
