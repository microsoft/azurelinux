Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-artifact-transfer
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
Name:           maven-artifact-transfer
Version:        0.11.0
Release:        2%{?dist}
Summary:        Apache Maven Artifact Transfer
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-artifact-transfer
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
Patch0:         0001-Compatibility-with-Maven-3.0.3-and-later.patch
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-codec
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  guava20
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  maven-common-artifact-filters
BuildRequires:  maven-lib
BuildRequires:  maven-resolver-api
BuildRequires:  maven-resolver-impl
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
BuildRequires:  slf4j
BuildRequires:  unzip
BuildRequires:  xbean
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
An API to either install or deploy artifacts with Maven 3.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch0 -p1

%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin

# We don't want to support legacy Maven versions (older than 3.1)
%pom_remove_dep org.sonatype.aether:
find -name Maven30\*.java -delete

%build
mkdir -p lib
build-jar-repository -s lib \
	atinject \
	commons-cli \
	commons-codec \
	guava20/guava-20.0 \
	guice/google-guice-no_aop \
	jdom2/jdom2 \
	maven-common-artifact-filters/maven-common-artifact-filters \
	maven/maven-artifact \
	maven/maven-core \
	maven/maven-model \
	maven-resolver/maven-resolver-api \
	maven-resolver/maven-resolver-impl \
	maven-resolver/maven-resolver-util \
	objectweb-asm/asm \
	org.eclipse.sisu.inject \
	org.eclipse.sisu.plexus \
	plexus-classworlds \
	plexus/cli \
	plexus-containers/plexus-component-annotations \
	plexus-metadata-generator \
	plexus/utils \
	qdox \
	slf4j/api \
	slf4j/simple \
	xbean/xbean-reflect

%{ant} \
%if %{without tests}
	-Dtest.skip=true \
%endif
	package javadoc

%{mvn_artifact} pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.11.0-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 0.11.0
- Modified patch:
  * 0001-Compatibility-with-Maven-3.0.3-and-later.patch
    + rediff to changed context
* Tue Mar 26 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-artifact-transfer 0.9.0
- Generate and customize ant build.xml file
