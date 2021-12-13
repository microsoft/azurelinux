Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-common-artifact-filters
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

%bcond_with tests
Name:           maven-common-artifact-filters
Version:        3.0.1
Release:        2%{?dist}
Summary:        Maven Common Artifact Filters
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
Patch0:         0001-Remove-Maven-3.0-specific-code.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-lib
BuildRequires:  maven-resolver-api
BuildRequires:  maven-resolver-util
BuildRequires:  maven-shared-utils
BuildRequires:  sisu-plexus
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-lang3
BuildRequires:  easymock
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  plexus-archiver
BuildRequires:  plexus-utils
%endif

%description
A collection of ready-made filters to control inclusion/exclusion of artifacts
during dependency resolution.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch0 -p1

# We don't want to support legacy Maven versions (older than 3.1)
%pom_remove_dep org.sonatype.sisu:
%pom_remove_dep org.sonatype.aether:
find -name SonatypeAether\*.java -delete

%build
mkdir -p lib
build-jar-repository -s lib \
    maven/maven-artifact \
    maven/maven-core \
    maven/maven-model \
    maven/maven-model-builder \
    maven/maven-plugin-api \
    maven-resolver/maven-resolver-api \
    maven-resolver/maven-resolver-util \
    maven-shared-utils/maven-shared-utils \
    org.eclipse.sisu.plexus
%if %{with tests}
build-jar-repository -s lib \
    commons-lang3 \
    easymock \
    maven-plugin-testing/maven-plugin-testing-harness \
    plexus/archiver \
    plexus/utils
%endif

%{ant} \
%if %{without tests}
    -Dtest.skip=true \
%endif
    jar javadoc

%mvn_artifact pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.1-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-common-artifact-filters 3.0.1
- Generate and customize the ant build.xml file
