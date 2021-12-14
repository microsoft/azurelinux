Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-verifier
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
Name:           maven-verifier
Version:        1.6
Release:        3%{?dist}
Summary:        Test harness for Maven integration tests
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-verifier
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  junit
BuildRequires:  maven-shared-utils
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Provides a test harness for Maven integration tests.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

%build
mkdir -p lib
build-jar-repository -s lib \
  maven-shared-utils/maven-shared-utils \
  junit

%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Apr  9 2019 Jan Engelhardt <jengelh@inai.de>
- Avoid name repetition in summary.
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-verifier 1.6
- Generate and customize the ant build.xml file
