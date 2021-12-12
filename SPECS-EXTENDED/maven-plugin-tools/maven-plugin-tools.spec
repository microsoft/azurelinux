Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-plugin-tools
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


Name:           maven-plugin-tools
Version:        3.6.0
Release:        2%{?dist}
Summary:        Maven Plugin Tools
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/plugin-tools/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugin-tools/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.tar.xz
Patch0:         0001-Avoid-duplicate-MOJO-parameters.patch
Patch1:         0002-Deal-with-nulls-from-getComment.patch
Patch2:         0003-Port-to-plexus-utils-3.0.24.patch
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  atinject
BuildRequires:  bsh2
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  jtidy
BuildRequires:  junit
BuildRequires:  maven-lib
BuildRequires:  maven-reporting-api
BuildRequires:  modello
BuildRequires:  objectweb-asm
BuildRequires:  plexus-ant-factory
BuildRequires:  plexus-archiver
BuildRequires:  plexus-bsh-factory
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  qdox
BuildRequires:  sisu-inject
BuildRequires:  sisu-plexus
BuildRequires:  unzip
BuildRequires:  velocity
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildArch:      noarch

%description
The Maven Plugin Tools contains the necessary tools to be able to produce Maven
Plugins in a variety of languages.

%package -n maven-plugin-annotations
Summary:        Maven Plugin Java 5 Annotations
Group:          Development/Libraries/Java

%description -n maven-plugin-annotations
This package contains Java 5 annotations to use in Mojos.

%package annotations
Summary:        Maven Plugin Tool for Annotations
Group:          Development/Libraries/Java

%description annotations
This package provides Java 5 annotation tools for use with Apache Maven.

%package ant
Summary:        Maven Plugin Tool for Ant
Group:          Development/Libraries/Java

%description ant
Descriptor extractor for plugins written in Ant.

%package api
Summary:        Maven Plugin Tools APIs
Group:          Development/Libraries/Java

%description api
The Maven Plugin Tools API provides an API to extract information from
and generate documentation for Maven Plugins.

%package beanshell
Summary:        Maven Plugin Tool for Beanshell
Group:          Development/Libraries/Java

%description beanshell
Descriptor extractor for plugins written in Beanshell.

%package generators
Summary:        Maven Plugin Tools Generators
Group:          Development/Libraries/Java

%description generators
The Maven Plugin Tools Generators provides content generation
(documentation, help) from plugin descriptor.

%package java
Summary:        Maven Plugin Tool for Java
Group:          Development/Libraries/Java

%description java
Descriptor extractor for plugins written in Java.
%package model
Summary:        Maven Plugin Metadata Model
Group:          Development/Libraries/Java

%description model
The Maven Plugin Metadata Model provides an API to play with the Metadata
model.

%package -n maven-script-ant
Summary:        Maven Ant Mojo Support
Group:          Development/Libraries/Java

%description -n maven-script-ant
This package provides %{summary}, which write Maven plugins with
Ant scripts.

%package -n maven-script-beanshell
Summary:        Maven Beanshell Mojo Support
Group:          Development/Libraries/Java

%description -n maven-script-beanshell
This package provides %{summary}, which write Maven plugins with
Beanshell scripts.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java
Provides:       %{name}-javadocs = %{version}-%{release}
Obsoletes:      %{name}-javadocs < %{version}-%{release}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%pom_remove_plugin -r :maven-enforcer-plugin

%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>"

# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope='test']"

%pom_change_dep org.easymock:easymock:: :::test maven-plugin-tools-annotations

%{mvn_package} :maven-plugin-tools __noinstall
%{mvn_package} :maven-script __noinstall
%{mvn_package} :{*} @1

%build
mkdir -p lib
build-jar-repository -s lib \
	ant \
	ant-launcher \
	atinject \
	bsh2/bsh \
	commons-cli \
	guava20/guava-10.0 \
	guice/google-guice-no_aop \
	jdom2/jdom2 \
	jtidy \
	junit \
	maven/maven-artifact \
	maven/maven-compat \
	maven/maven-core \
	maven/maven-model \
	maven/maven-plugin-api \
	maven-reporting-api/maven-reporting-api \
	objectweb-asm/asm \
	objectweb-asm/asm-commons \
	org.eclipse.sisu.inject \
	org.eclipse.sisu.plexus \
	plexus/ant-factory \
	plexus/archiver \
	plexus/bsh-factory \
	plexus-classworlds \
	plexus/cli \
	plexus-containers/plexus-component-annotations \
	plexus-metadata-generator \
	plexus/utils \
	plexus-velocity/plexus-velocity \
	qdox \
	velocity \
	xbean/xbean-reflect

	ln -s $(xmvn-resolve com.sun:tools) lib/

%{ant} \
	-Dtest.skip=true \
	package javadoc

%mvn_artifact pom.xml
%mvn_artifact maven-script/pom.xml

mkdir -p target/site/apidocs
for i in \
	maven-plugin-annotations \
	maven-plugin-tools-annotations \
	maven-plugin-tools-api \
	maven-plugin-tools-generators \
	maven-plugin-tools-java; do
  %{mvn_artifact} ${i}/pom.xml ${i}/target/${i}-%{version}.jar
  if [ -d ${i}/target/site/apidocs ]; then
    cp -r ${i}/target/site/apidocs target/site/apidocs/${i}
  fi
done
for i in \
	maven-plugin-tools-ant \
	maven-plugin-tools-beanshell \
	maven-plugin-tools-model \
	maven-script-ant \
	maven-script-beanshell; do
  %{mvn_artifact} maven-script/${i}/pom.xml maven-script/${i}/target/${i}-%{version}.jar
  if [ -d maven-script/${i}/target/site/apidocs ]; then
    cp -r maven-script/${i}/target/site/apidocs target/site/apidocs/${i}
  fi
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -n maven-plugin-annotations -f .mfiles-maven-plugin-annotations

%files annotations -f .mfiles-maven-plugin-tools-annotations
%license LICENSE NOTICE

%files ant -f .mfiles-maven-plugin-tools-ant

%files api -f .mfiles-maven-plugin-tools-api
%license LICENSE NOTICE

%files beanshell -f .mfiles-maven-plugin-tools-beanshell

%files generators -f .mfiles-maven-plugin-tools-generators

%files java -f .mfiles-maven-plugin-tools-java

%files model -f .mfiles-maven-plugin-tools-model
%license LICENSE NOTICE

%files -n maven-script-ant -f .mfiles-maven-script-ant
%license LICENSE NOTICE

%files -n maven-script-beanshell -f .mfiles-maven-script-beanshell
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 18 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.6.0-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Switch from java-1_8_0-openjdk-devel to java-1.8.0-openjdk-devel.

* Mon Nov 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream 3.6.0
  * allow building with java > 1.8 too against objectweb-asm 7.2
  * maven-plugin-tools-javadoc component does not exist any more
  * Renamed the package of documentation to
    maven-plugin-tools-javadoc since there is no name clash any
    more and it allows smooth upgrade
- Removed patch:
  * fix-getPluginsAsMap.patch
    + fix is present in the updated sources
* Fri Mar 29 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-plugin-tools 3.5.1
- Generate and customize ant build files
- Do not build maven-plugin-plugin in this spec, since it has
  circular dependency on itself
