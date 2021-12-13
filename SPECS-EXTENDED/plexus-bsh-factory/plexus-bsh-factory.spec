Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-bsh-factory
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


%define parent plexus
%define subname bsh-factory
%define base_ver 1.0
%define alpha_ver 7
%define namedversion %{base_ver}-alpha-%{alpha_ver}
Name:           %{parent}-%{subname}
Version:        1.0~a7
Release:        2%{?dist}
Summary:        Plexus Bsh component factory
License:        MIT
Group:          Development/Libraries/Java
URL:            https://codehaus-plexus.github.io
# sources are here https://mvnrepository.com/artifact/org.codehaus.plexus/plexus-bsh-factory 
# jar or pom files that need to be changed into tarball
Source0:        %{name}-src.tar.gz
Source1:        %{name}-build.xml
Source3:        plexus-bsh-factory-license.txt
Patch1:         %{name}-encodingfix.patch
Patch2:         0001-Migrate-to-plexus-containers-container-default.patch
BuildRequires:  ant
BuildRequires:  bsh2
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-classworlds >= 2
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
Requires:       mvn(bsh:bsh)
Requires:       mvn(classworlds:classworlds)
Requires:       mvn(org.codehaus.plexus:plexus-container-default)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch

%description
Bsh component class creator for Plexus.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}

%patch1 -b .sav
%patch2 -p1
cp release-pom.xml pom.xml
cp %{SOURCE1} build.xml
cp -p %{SOURCE3} .

%build
mkdir -p lib

build-jar-repository -s lib plexus/classworlds plexus/utils plexus-containers/plexus-container-default bsh2/bsh
%{ant} \
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{parent}
install -pm 0644 target/%{name}-%{namedversion}.jar %{buildroot}%{_javadir}/%{parent}/%{subname}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{parent}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{parent}/%{subname}.pom
%add_maven_depmap %{parent}/%{subname}.pom %{parent}/%{subname}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license plexus-bsh-factory-license.txt

%files javadoc
%license plexus-bsh-factory-license.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0~a7-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0~a7-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Mar  8 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-bsh-factory 1.0-alpha-7
- Generate and customize ant build.xml file
