Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-archiver
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
Name:           maven-archiver
Version:        3.5.0
Release:        2%{?dist}
Summary:        Maven Archiver
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-archiver/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
Patch0:         0001-Port-tests-to-Eclipse-Aether.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-lib
BuildRequires:  maven-shared-utils
BuildRequires:  plexus-archiver >= 4.2.0
BuildRequires:  plexus-interpolation >= 1.25
BuildRequires:  plexus-utils >= 3.3.0
BuildRequires:  sisu-plexus
BuildRequires:  unzip
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-compress
BuildRequires:  apache-commons-io
BuildRequires:  assertj-core
BuildRequires:  maven-resolver-api
BuildRequires:  plexus-io
BuildRequires:  plexus-utils
%endif

%description
The Maven Archiver is used by other Maven plugins
to handle packaging

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch0 -p1

%build
mkdir -p lib
build-jar-repository -s lib \
  org.eclipse.sisu.plexus \
  maven-shared-utils/maven-shared-utils \
  maven/maven-artifact maven/maven-core \
  maven/maven-model \
  plexus/interpolation \
  plexus/archiver

%if %{with tests}
  build-jar-repository -s lib \
    assertj-core/assertj-core \
    maven-resolver/maven-resolver-api \
    maven/maven-settings \
    plexus/io \
    commons-compress \
    commons-io \
    plexus/utils
%endif

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
%license LICENSE
%doc NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.5.0-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 3.5.0
- Removed patch:
  * 0002-MSHARED-448-Skip-failing-assertion.patch
    + not needed with this version
- Modified patch:
  * 0001-Port-tests-to-Eclipse-Aether.patch
    + rediff to changed context
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-archiver 3.2.0
- Generate and customize the ant build.xml file
