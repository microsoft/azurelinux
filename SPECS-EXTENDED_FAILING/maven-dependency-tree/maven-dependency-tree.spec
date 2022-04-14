Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-dependency-tree
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


Name:           maven-dependency-tree
Version:        3.0
Release:        2%{?dist}
Summary:        Maven dependency tree artifact
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  javapackages-local
BuildRequires:  jdom2
BuildRequires:  maven-lib
BuildRequires:  maven-resolver-api
BuildRequires:  maven-resolver-util
BuildRequires:  objectweb-asm
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
BuildRequires:  qdox
BuildRequires:  sisu-inject
BuildRequires:  sisu-plexus
BuildRequires:  unzip
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch

%description
Apache Maven dependency tree artifact. Originally part of maven-shared.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

find -name Maven3DependencyGraphBuilder.java -delete
%pom_remove_dep org.sonatype.aether:

%pom_remove_plugin :apache-rat-plugin

%build
mkdir -p lib
build-jar-repository -s lib \
  atinject \
  commons-cli \
  guice/google-guice-no_aop \
  guava20/guava-10.0 \
  jdom2/jdom2 \
  maven/maven-artifact \
  maven/maven-core \
  maven-resolver/maven-resolver-api \
  maven-resolver/maven-resolver-util \
  objectweb-asm/asm org.eclipse.sisu.inject \
  org.eclipse.sisu.plexus \
  plexus-classworlds \
  plexus/cli \
  plexus-containers/plexus-component-annotations \
  plexus-metadata-generator \
  plexus/utils \
  qdox \
  xbean/xbean-reflect

%{ant} \
  -Dtest.skip=true \
  jar javadoc

%{mvn_artifact} pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE
%doc NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-dependency-tree 3.0
- Generate and customize the ant build.xml file
