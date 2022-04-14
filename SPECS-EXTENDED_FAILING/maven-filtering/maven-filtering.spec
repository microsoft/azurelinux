Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-filtering
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


Name:           maven-filtering
Version:        3.1.1
Release:        2%{?dist}
Summary:        Shared component providing resource filtering
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/%{name}/index.html
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  jsr-305
BuildRequires:  maven-lib
BuildRequires:  maven-shared-utils
BuildRequires:  objectweb-asm
BuildRequires:  plexus-build-api
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-interpolation
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
These Plexus components have been built from the filtering process/code in
Maven Resources Plugin. The goal is to provide a shared component for all
plugins that needs to filter resources.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

%build
mkdir -p lib
build-jar-repository -s lib \
    atinject \
    commons-cli \
    guava20/guava-10.0 \
    guice/google-guice-no_aop \
    jdom2/jdom2 \
    jsr-305 \
    maven/maven-core \
    maven/maven-model \
    maven/maven-settings \
    maven-shared-utils/maven-shared-utils \
    objectweb-asm/asm \
    org.eclipse.sisu.inject \
    org.eclipse.sisu.plexus \
    plexus-classworlds \
    plexus/cli \
    plexus-containers/plexus-component-annotations \
    plexus/interpolation \
    plexus-metadata-generator \
    plexus/plexus-build-api \
    plexus/utils \
    qdox \
    xbean/xbean-reflect

# Tests use a package that is no longer present in plexus-build-api (v0.0.7)
%{ant} \
  -Dtest.skip=true \
  jar javadoc

%{mvn_artifact} pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.1.1-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-filtering 3.1.1
- Generate and customize the ant build.xml file
