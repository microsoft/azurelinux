Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-file-management
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
Name:           maven-file-management
Version:        3.0.0
Release:        2%{?dist}
Summary:        Maven File Management API
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/file-management
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/file-management/%{version}/file-management-%{version}-source-release.zip
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-lib
BuildRequires:  maven-shared-io
BuildRequires:  maven-shared-utils
BuildRequires:  modello
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Provides a component for plugins to easily resolve project dependencies.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n file-management-%{version}
cp %{SOURCE1} build.xml

%build
mkdir -p lib
build-jar-repository -s lib \
	maven/maven-plugin-api \
	maven-shared-io/maven-shared-io \
	maven-shared-utils/maven-shared-utils \
	plexus-containers/plexus-container-default \
	plexus/utils

%{ant} \
%if %{without tests}
	-Dtest.skip=true \
%endif
	jar javadoc

%{mvn_artifact} pom.xml target/file-management-%{version}.jar

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

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.0-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Mar 26 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-file-management 3.0.0
- Generate and customize ant build.xml file
