Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-shared-io
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


Name:           maven-shared-io
Version:        3.0.0
Release:        2%{?dist}
Summary:        API for I/O support like logging, download or file scanning
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-shared-io
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
# Rejected upstream: https://issues.apache.org/jira/browse/MSHARED-490
Patch0:         0001-Fix-running-tests-with-Maven-3.3.9.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-lib
BuildRequires:  maven-shared-utils
BuildRequires:  maven-wagon-provider-api
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch

%description
API for I/O support like logging, download or file scanning.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch0 -p1

%pom_add_dep org.codehaus.plexus:plexus-container-default::provided

%build
mkdir -p lib
build-jar-repository -s lib \
  maven/maven-compat \
  maven/maven-core \
  maven/maven-artifact \
  maven/maven-plugin-api \
  maven-wagon/provider-api \
  maven-shared-utils/maven-shared-utils \
  plexus/utils \
  plexus-containers/plexus-container-default

# Some of the tests cannot run outside maven
%{ant} \
  -Dtest.skip=true \
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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.0-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-shared-io 3.0.0
- Generate and customize the ant build.xml file
