Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-resolver
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


%bcond_with tests
Name:           maven-resolver
Version:        1.4.1
Release:        2%{?dist}
Summary:        Apache Maven Artifact Resolver library
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/resolver/
Source0:        http://archive.apache.org/dist/maven/resolver/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.tar.xz
Patch0:         maven-resolver-1.3.1-java8compat.patch
BuildRequires:  ant
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  httpcomponents-client
BuildRequires:  httpcomponents-core
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jcl-over-slf4j
BuildRequires:  maven-wagon-provider-api
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils
BuildRequires:  sisu-inject
BuildRequires:  sisu-plexus
BuildRequires:  slf4j
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  cglib
BuildRequires:  guava20
BuildRequires:  mockito
BuildRequires:  objectweb-asm
BuildRequires:  objenesis
BuildRequires:  plexus-containers-component-annotations
%endif

%description
Apache Maven Artifact Resolver is a library for working with artifact
repositories and dependency resolution. Maven Artifact Resolver deals with the
specification of local repository, remote repository, developer workspaces,
artifact transports and artifact resolution.

%package api
Summary:        Maven Artifact Resolver API
Group:          Development/Libraries/Java

%description api
The application programming interface for the repository system.

%package spi
Summary:        Maven Artifact Resolver SPI
Group:          Development/Libraries/Java

%description spi
The service provider interface for repository system implementations and
repository connectors.

%package util
Summary:        Maven Artifact Resolver Utilities
Group:          Development/Libraries/Java

%description util
A collection of utility classes to ease usage of the repository system.

%package impl
Summary:        Maven Artifact Resolver Implementation
Group:          Development/Libraries/Java

%description impl
An implementation of the repository system.

%package test-util
Summary:        Maven Artifact Resolver Test Utilities
Group:          Development/Libraries/Java

%description test-util
A collection of utility classes to ease testing of the repository system.

%package connector-basic
Summary:        Maven Artifact Resolver Connector Basic
Group:          Development/Libraries/Java

%description connector-basic
A repository connector implementation for repositories using URI-based layouts.

%package transport-classpath
Summary:        Maven Artifact Resolver Transport Classpath
Group:          Development/Libraries/Java

%description transport-classpath
A transport implementation for repositories using classpath:// URLs.

%package transport-file
Summary:        Maven Artifact Resolver Transport File
Group:          Development/Libraries/Java

%description transport-file
A transport implementation for repositories using file:// URLs.

%package transport-http
Summary:        Maven Artifact Resolver Transport HTTP
Group:          Development/Libraries/Java

%description transport-http
A transport implementation for repositories using http:// and https:// URLs.

%package transport-wagon
Summary:        Maven Artifact Resolver Transport Wagon
Group:          Development/Libraries/Java

%description transport-wagon
A transport implementation based on Maven Wagon.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
This package provides %{summary}.

%prep
%setup -q -a1
%patch0 -p1

# tests require jetty 7
%pom_remove_dep :::test maven-resolver-transport-http
rm -r maven-resolver-transport-http/src/test

%pom_disable_module maven-resolver-demos

# generate OSGi manifests
for pom in $(find -mindepth 2 -name pom.xml) ; do
  %pom_add_plugin "org.apache.felix:maven-bundle-plugin" $pom \
  "<configuration>
    <instructions>
      <Bundle-SymbolicName>\${project.groupId}$(sed 's:./maven-resolver::;s:/pom.xml::;s:-:.:g' <<< $pom)</Bundle-SymbolicName>
      <Export-Package>!org.eclipse.aether.internal*,org.eclipse.aether*</Export-Package>
      <_nouses>true</_nouses>
    </instructions>
  </configuration>
  <executions>
    <execution>
      <id>create-manifest</id>
      <phase>process-classes</phase>
      <goals><goal>manifest</goal></goals>
    </execution>
  </executions>"
done
%pom_add_plugin "org.apache.maven.plugins:maven-jar-plugin" pom.xml \
"<configuration>
  <archive>
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
  </archive>
</configuration>"

%{mvn_package} :maven-resolver
%{mvn_package} :maven-resolver-{*}  @1
%{mvn_alias} 'org.apache.maven.resolver:maven-resolver{*}' 'org.eclipse.aether:aether@1'
%{mvn_file} ':maven-resolver{*}' %{name}/maven-resolver@1 aether/aether@1

# Try to avoid sucking in dependencies on packages that are not built at this moment
%pom_remove_parent .
%pom_remove_plugin :maven-jar-plugin .

%build
mkdir -p lib
build-jar-repository -s lib \
  atinject \
  guice/google-guice-no_aop \
  httpcomponents/httpclient \
  httpcomponents/httpcore \
  maven-wagon/provider-api \
  org.eclipse.sisu.inject \
  org.eclipse.sisu.plexus \
  plexus-classworlds \
  plexus/utils \
  slf4j/api
%if %{with tests}
build-jar-repository -s lib \
  cglib/cglib \
  guava20/guava-20.0 \
  mockito/mockito-core \
  objectweb-asm/asm \
  objenesis/objenesis \
  plexus-containers/plexus-component-annotations \
  slf4j/simple
%endif
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  package javadoc

%mvn_artifact pom.xml

mkdir -p target/site/apidocs
for i in api spi test-util util impl connector-basic transport-classpath transport-file transport-http transport-wagon; do
  cp -r %{name}-${i}/target/site/apidocs target/site/apidocs/%{name}-${i}
  %{mvn_artifact} %{name}-${i}/pom.xml %{name}-${i}/target/%{name}-${i}-%{version}.jar
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files api -f .mfiles-api
%license LICENSE NOTICE

%files spi -f .mfiles-spi

%files util -f .mfiles-util

%files impl -f .mfiles-impl

%files test-util -f .mfiles-test-util

%files connector-basic -f .mfiles-connector-basic

%files transport-classpath -f .mfiles-transport-classpath

%files transport-file -f .mfiles-transport-file

%files transport-http -f .mfiles-transport-http

%files transport-wagon -f .mfiles-transport-wagon

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.4.1-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Dec  9 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.4.1
* Wed Mar 20 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-resolver 1.3.1
- Generate and customize the ant build files
- Added patch:
  * maven-resolver-1.3.1-java8compat.patch
    + avoid calling APIs added in Java 9
