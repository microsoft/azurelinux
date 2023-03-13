Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-component-api
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


%define base_ver 1.0
%define alpha_ver 15
%define project_version %{base_ver}-alpha-%{alpha_ver}
Name:           plexus-component-api
Version:        %{base_ver}~alpha%{alpha_ver}
Release:        5%{?dist}
Summary:        Plexus Component API
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            https://mvnrepository.com/artifact/org.codehaus.plexus/plexus-component-api
#svn export http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.0-alpha-15/plexus-component-api/ plexus-component-api-1.0-alpha-15
#tar cJf plexus-component-api-1.0-alpha-15.tar.xz plexus-component-api-1.0-alpha-15/
Source0:        %{_mariner_sources_url}/%{name}-%{project_version}.tar.xz
Source1:        %{name}-build.xml
Source2:        %{name}-LICENSE.txt
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.6
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-classworlds
Requires:       plexus-classworlds
BuildArch:      noarch

%description
Plexus Component API

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{project_version}
cp %{SOURCE1} build.xml
cp %{SOURCE2} ./LICENSE.txt

%pom_remove_parent

%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>"

%build
mkdir -p lib
build-jar-repository -s lib plexus/classworlds
%{ant} jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-%{project_version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Mon Mar 13 2023 Sindhu Karr <lakarri@microsoft.com> - 1.0~alpha15-5
- Runtime requirement modified from mvn artifact to plexus-classworlds package

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.0~alpha15-4
- Updated source URL.

* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.0~alpha15-3
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0~alpha15-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0~alpha15-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Mar  6 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-component-api 1.0-alpha-15
- Generate and customize ant build.xml file to be able to build
  without maven
