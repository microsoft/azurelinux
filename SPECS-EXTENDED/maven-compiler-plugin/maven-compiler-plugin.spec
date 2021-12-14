Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-compiler-plugin
#
# Copyright (c) 2019 SUSE LLC
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


%global flavor bootstrap
%if "%{flavor}" == "bootstrap"
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif
%global base_name maven-compiler-plugin
Version:        3.8.1
Release:        3%{?dist}
Summary:        Maven Compiler Plugin
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/plugins/maven-compiler-plugin
Source0:        http://archive.apache.org/dist/maven/plugins/%{base_name}-%{version}-source-release.zip
Source1:        %{base_name}-build.xml
Patch0:         %{base_name}-bootstrap-resources.patch
Patch1:         00-plexus-languages-1.0.patch
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-lib
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-shared-incremental
BuildRequires:  maven-shared-utils
BuildRequires:  plexus-compiler
BuildRequires:  plexus-languages
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildArch:      noarch
%if %{with bootstrap}
Name:           %{base_name}-bootstrap
Provides:       %{base_name} = %{version}-%{release}
BuildRequires:  ant
%else
Name:           %{base_name}
BuildRequires:  xmvn
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-javadoc-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-resources-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
Obsoletes:      %{base_name}-bootstrap
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
%endif

%description
The Compiler Plugin is used to compile the sources of your project.

%if %{without bootstrap}
%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.
%endif

%prep
%setup -q -n %{base_name}-%{version}
%if %{with bootstrap}
cp %{SOURCE1} build.xml
%patch0 -p1
%endif
%patch1 -p1

%pom_remove_dep :::test

%build
%if %{with bootstrap}
mkdir -p lib
build-jar-repository -s lib \
	maven/maven-artifact \
	maven/maven-core \
	maven/maven-model \
	maven/maven-plugin-api \
	maven-plugin-tools/maven-plugin-annotations \
	maven-shared-incremental/maven-shared-incremental \
	maven-shared-utils/maven-shared-utils \
	plexus-compiler/plexus-compiler-api \
	plexus-compiler/plexus-compiler-javac \
	plexus-compiler/plexus-compiler-manager \
	plexus-languages/plexus-java
%{ant} -Dtest.skip=true jar
%else
xmvn --batch-mode --offline \
	-Dmaven.test.skip=true \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-Dmaven.compiler.release=7 \
%endif
	package org.apache.maven.plugins:maven-javadoc-plugin:aggregate
%endif

%{mvn_artifact} pom.xml target/%{base_name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%if %{without bootstrap}
%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.1-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.8.1-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Switch to bootstrap mode.
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Nov 29 2019 Fridrich Strba <fstrba@suse.com>
- Remove all dependencies with scope test, since we are disabling
  tests
* Mon Nov 25 2019 Fridrich Strba <fstrba@suse.com>
- Update to upstream version 3.8.1
- Modified patch:
  * maven-compiler-plugin-bootstrap-resources.patch
    + Regenerate from the non-bootstrap build
* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * 00-plexus-languages-1.0.patch
    + fix build against plexus-java >= 1.0
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-compiler-plugin 3.8.0
- Package as a multibuild package in order to allow bootstapping
- Generate and customize ant build.xml file for the bootstrap
  version
- Added patch:
  * maven-compiler-plugin-bootstrap-resources.patch
    + For the bootstrap version, add the pre-generated resources
    that need maven-plugin-plugin
