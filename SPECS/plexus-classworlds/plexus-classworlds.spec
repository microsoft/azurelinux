#
# spec file for package plexus
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
%global short_name classworlds
%bcond_with tests
Summary:        Plexus Classworlds Classloader Framework
Name:           plexus-%{short_name}
Version:        2.5.2
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-classworlds
Source0:        https://github.com/sonatype/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       %{short_name} = %{version}-%{release}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  commons-logging
BuildRequires:  xml-apis
%endif

%description
Classworlds is a framework for container developers
who require complex manipulation of Java's ClassLoaders.
Java's native ClassLoader mechanisms and classes can cause
much headache and confusion for certain types of
application developers. Projects which involve dynamic
loading of components or otherwise represent a 'container'
can benefit from the classloading control provided by
classworlds.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
cp %{SOURCE1} build.xml
%if %{with tests}
mkdir -p target/test-lib
rm -f target/test-lib/{ant-1.9.0,commons-logging-1.0.3,xml-apis-1.3.02}.jar
ln -s $(build-classpath ant/ant) target/test-lib/ant-1.9.0.jar
ln -s $(build-classpath commons-logging) target/test-lib/commons-logging-1.0.3.jar
ln -s $(build-classpath xml-apis) target/test-lib/xml-apis-1.3.02.jar
%endif

%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-dependency-plugin

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" .

%build
%{ant} \
%if %{without tests}
    -Dtest.skip=true \
%endif
    jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf ../%{name}.jar %{buildroot}%{_javadir}/plexus/%{short_name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a %{short_name}:%{short_name}
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt LICENSE-2.0.txt
%{_javadir}/plexus
%{_javadir}/%{short_name}.jar

%files javadoc
%license LICENSE.txt LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.5.2-4
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.2-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.5.2-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.

* Thu Feb 14 2019 Fridrich Strba <fstrba@suse.com>
- Rename package to plexus-classworlds
- Ugrade to version 2.5.2
- Make building with tests optional as to avoid/shorten build
  cycles

* Wed May 16 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Added patch:
  * classworlds-1.1-deprecated.patch
    + File.toURL() is deprecated

* Mon Sep 18 2017 fstrba@suse.com
- Specify java source and target level 1.6 in order to allow build
  with jdk9
- Clean spec file

* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
- Fixed requires
- Removed maven conditions
- Spec file cleaned

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Wed Aug 28 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
- use pom file from repo1.maven.org

* Thu May 10 2012 cfarrell@suse.com
- license update: BSD-3-Clause
  Open Source is not a recognised license. Use the proper license
  (BSD-3-Clause) in SPDX format

* Wed Jun  3 2009 mvyskocil@suse.cz
- Initial SUSE packaging from jpackage.org 5.0
